#from django.conf.urls import url
from django.urls import re_path as url
from . import views
from django.urls import include, path

# urls list 
urlpatterns = [
 path("auth",views.get_token),
 path('register',views.register,name='register'),
 path('authenticate',views.authenticate,name='authenticate'),
 path('userlogout',views.userlogout,name='userlogout'),
 path('smsCode',views.smsCode,name='smsCode'),
]
