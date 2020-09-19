import random
import string
from django_reflinks.models import ReferralLink, ReferralHit
from decimal import Decimal
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from .forms import UserCreationForm, SignUpForm

from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .forms import ProfileForm, ReferralLinkForm, SignUpForm
from .models import Profile, Wallet
from user_visit.models import UserVisit






def ref_link_form(request):
    form = ReferralLinkForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('/dashboard')
        form = ReferralLinkForm()
    template_name = 'core/ref_link.html'
    context = {'form': form}
    return render(request, template_name, context)  


def get_referral(request, referral_link):
    try:
        referral = Referral.objects.get(referral_link=referral_link)
        return referral
    except ObjectDoesNotExist:
        messages.info(request, "This referral_link does not exist")
        return redirect("/accounts/signup")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)             
        if form.is_valid():
            u_email = str(request.POST.get('email'))
            print(u_email)
            if '@' not in u_email:
                email_error = 'Email is not valid'
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form':form,'email_error': email_error})
            else:
                print('wrong')
                form.save()
                messages.success(request, 'Your Account was created successfully!')
                return redirect('/accounts/login')
        else:
            #Error messages for username
            u_name_list = []
            u_name = request.POST.get('username')
            u_name_obj = User.objects.filter(Q(username=u_name))
            if u_name_obj.exists():
                name_exists = 'Username already exists'
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form':form,'name_exists': name_exists})

            #Error messages for email
            u_email = str(request.POST.get('email'))
            print(u_email)
            
            if '@' not in u_email:
                print('baller')
            else:
                print('wrong')
            #Error messages for password
            if len(request.POST.get('password1')) < 8:
                too_short_password = "Password characters shouldn't be less than 8"
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form':form,'too_short':too_short_password}) 
            elif request.POST.get('password1') != request.POST.get('password2'):
                not_the_same_password = 'Passwords not the same'
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form':form,'not_the_same_password': not_the_same_password}) 
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form':form}) 

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")
 


def sellers_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        ref_form = ReferralForm(request.POST or None)
        if form.is_valid() and profile_form.is_valid():

            # form.save()
            user = form.save()
            user.profile.store_name = profile_form.cleaned_data.get('store_name')
            # user.profile.location = profile_form.cleaned_data.get('location')
            user.profile.save() 
            # profile_form.save()
            try:
                user.referral.referral_link = ref_form.cleaned_data['referral_link']
                order = Referral.objects.get(
                         user=self.request.user)
                order.coupon = get_referral(self.request, referral_link)
                order.save()
                user.referral.save()
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")
            messages.success(request, 'Your Account was created successfully!')
            return redirect('/login')

    else:
        form = UserCreationForm()
        profile_form = ProfileForm()
        ref_form = ReferralForm()
    return render(request, 'core/sellers-signup.html', {'form':form, 'profile_form': profile_form,'ref_form': ref_form}) 


@login_required
def dashboard(request):

    '''This function takes care of everything concerning the user,
    wallet functions and profile'''

    prof = Profile.objects.all()
    wallet = Wallet.objects.filter(Q(user=request.user))
    try:
        obj_ref = ReferralLink.objects.get(user=request.user)  
        print(obj_ref)    
    except ReferralLink.DoesNotExist:
        obj_ref = ReferralLink(user=request.user)
        obj_ref = ReferralLink.objects.create(user=request.user, identifier=request.user.username)
        print(obj_ref,'---')

    #Except users that dont have referral's link yet
    try:
        ref_link = ReferralLink.objects.get(user=request.user)
        user_visit = UserVisit.objects.filter(Q(user=request.user))

        #get unique users, loop through user_visit and get the length of unique visit timestamp in the list
        user_visit_list = []
        for n in user_visit:
            n_loop = str(n.timestamp)[:10]
            user_visit_list.append(n_loop)
            unique_visit = list(set(user_visit_list))
        unique_visit = len(unique_visit)

        #slice referral link
        user_visit_fee = unique_visit*1000
        part_one = str(ref_link)[1:4]
        part_two = str(ref_link)[5:]
       
        signup_fee = 300
        ref_hit = ReferralHit.objects.filter(Q(next__icontains='/signup/')&Q(authenticated=False)&Q(referral_link=ref_link))
        try:
            obj = Wallet(user=request.user)        
        except Wallet.DoesNotExist:
            obj = Wallet(user=request.user)
            obj = Wallet.objects.create(user=request.user, signup_fee=400, daily_login_fee=0,referral_fee=0, facebook_share_fee=0)


        try:
            length =ref_hit.count()
            referral_fees = length * 1000
            ref_fee = wallet.update(referral_fee=referral_fees)
            for m in wallet:
                a = m.referral_fee
            signup_fees = 400
            signup_fee = wallet.update(signup_fee=signup_fees)

            for obj in wallet:
                s = obj.signup_fee
            daily_login = wallet.update(daily_login_fee = user_visit_fee)
            for login in wallet:
                d =login.daily_login_fee
            total = s + a + user_visit_fee
            template_name ='core/dashboard.html'
            context = {'prof': prof, 'ref_link': ref_link ,'ref_hit':ref_hit,'length': length,
            'referral_fee': referral_fees, 'signup_fee': s, 'total': total,'user_visit': d,
            'part_one': part_one, 'part_two': part_two}
            return render(request, template_name, context)
        except UnboundLocalError:
            obj = Wallet.objects.create(user=request.user, signup_fee=400, referral_fee=0, daily_login_fee=0, facebook_share_fee=0)
            for login in wallet:
                d =login.daily_login_fee
            print('unbound')
            template_name ='core/dashboard.html'
            signup_fee = 400
            total = 300
            referral_fee = 0
            total = signup_fee + user_visit_fee + referral_fees
            context = {'prof': prof, 'ref_link': ref_link ,'ref_hit':ref_hit,'signup_fee': signup_fee,
            'user_visit':user_visit_fee,'length':length,'part_one': part_one, 'part_two': part_two,
            'referral_fee':referral_fees,'total': total}
            return render(request, template_name, context)
        

        template_name ='core/dashboard.html'
        empty_list = []
        length = len(empty_list)
        total = 300
        referral_fee = 0
        context = {'prof': prof, 'ref_link': ref_link ,'ref_hit':ref_hit,'signup_fee': signup_fee,
        'user_visit':d,'length':length,'part_one': part_one, 'part_two': part_two,
        'referral_fee':referral_fee,'total': total}
        return render(request, template_name, context)
    except ObjectDoesNotExist:
        print('object does not exist')
    ref_hit = ReferralHit.objects.all()
    template_name ='core/dashboard.html'
    context = {'prof': prof ,'ref_hit':ref_hit}
    return render(request, template_name, context)

class ProfileDetailView(DetailView):
    queryset = User.objects.filter(is_active=True)
        
    template_name = 'core/dashboard.html'
    model = Profile

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username__iexact=username, is_active=True)



