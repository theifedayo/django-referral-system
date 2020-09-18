from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)






    def __str__(self):
        return self.user.username

class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    signup_fee = models.FloatField(default='400')
    referral_fee = models.FloatField(default='0')
    daily_login_fee = models.FloatField(default='0')
    facebook_share_fee = models.FloatField(default='0') 


    def __str__(self):
        return self.user.username
        


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


