from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm 



PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

# class SignUpForm(UserCreationForm):
#     email = forms.CharField(max_length=254, help_text='Required. Inform a valid email address.')
#     referral_link = forms.CharField(max_length = 30)
    


#     class Meta:
#         model = User
#         fields = ('username','referral_link','email','password1', 'password2', )
    

#     def signup(self, request, user): 
#          user.referral_link = self.cleaned_data['referral_link'] 
#          user.save() 
#          return user 

  
class CustomSignupForm(SignupForm): 
    # first_name = forms.CharField(max_length=30, label='First Name') 
    # last_name = forms.CharField(max_length=30, label='Last Name')
    referral_link = forms.CharField(max_length=30, label='Referral link')


    def signup(self, request, user): 
         # user.first_name = self.cleaned_data['first_name'] 
         # user.last_name = self.cleaned_data['last_name'] 
         user.referral_link = self.cleaned_data['referral_link'] 
         user.save() 
         return user 

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)

