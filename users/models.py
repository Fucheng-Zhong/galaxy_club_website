from django.db import models
from django.utils import timezone

class Profile(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField(unique=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)


        
