from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):

    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField(unique=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)




        
