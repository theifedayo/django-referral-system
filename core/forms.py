from django import forms
from django_countries.fields import CountryField
from django.forms import widgets
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm 
from .models import Profile
from django_reflinks.models import ReferralLink


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, help_text='Required. Inform a valid email address.')

class ReferralLinkForm(forms.ModelForm):
	class Meta:
		model = ReferralLink
		fields = ['identifier']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['store_name']


