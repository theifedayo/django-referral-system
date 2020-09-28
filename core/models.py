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
    wallet_id = models.CharField(max_length=25, unique=True)
    wallet_fee = models.FloatField(default='0') 
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
        

class Transfer(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    amount = models.CharField(max_length=25)
    user2 = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username





