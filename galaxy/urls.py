#from django.conf.urls import url
from django.urls import re_path as url
from . import views
from django.urls import include, path

urlpatterns = [
 path('requry_image',views.requry_image,name='requry_image'), #requry a image, return a url
 path('classify',views.classify_result,name='classify'),
]