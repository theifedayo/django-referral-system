from django import forms
from django_countries.fields import CountryField
from django.forms import widgets
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm 
from .models import Profile, Referral
from django_reflinks.models import ReferralLink


class ReferralLinkForm(forms.ModelForm):
	class Meta:
		model = ReferralLink
		fields = ['identifier']

class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['referral_link']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['store_name']


