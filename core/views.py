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

from .forms import ProfileForm, ReferralForm, ReferralLinkForm
from .models import Profile, Referral






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
# class HomeView(ListView):
#     model = Item
#     paginate_by = 10
#     template_name = "core/home.html"

def get_referral(request, referral_link):
    try:
        referral = Referral.objects.get(referral_link=referral_link)
        return referral
    except ObjectDoesNotExist:
        messages.info(request, "This referral_link does not exist")
        return redirect("/accounts/signup")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request, 'Your Account was created successfully!')
            return redirect('/accounts/login')

    else:
        form = UserCreationForm()
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
    prof = Profile.objects.all()
    ref = Referral.objects.all()
    try:
        ref_link = ReferralLink.objects.get(user=request.user)#get(identifier=user.identifier)
        ref_hit = ReferralHit.objects.all()
        template_name ='core/dashboard.html'
        context = {'prof': prof, 'ref_link': ref_link ,'ref_hit':ref_hit}
        return render(request, template_name, context)
    except ObjectDoesNotExist:
        pass
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



