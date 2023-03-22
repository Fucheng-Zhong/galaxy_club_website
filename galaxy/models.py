from django.db import models
from django.utils import timezone

# Create your models here.
class Galaxies(models.Model):
    galaxy_name = models.CharField(max_length= 50,verbose_name='galaxy_name')
    galaxy_num=models.CharField(max_length= 50, verbose_name='galaxy_num')
    raj=models.FloatField (default=0,verbose_name='raj')
    decj=models.FloatField(default=0,verbose_name='decj')
    classify_num=models.IntegerField(default=0,verbose_name='classified_num')
    hope_classify_num=models.IntegerField(default=5,verbose_name='hope_classify_num')
    created_time = models.DateTimeField(auto_now_add=True)
    last_change_time = models.DateTimeField(default=timezone.now)


class UserClassifyRecord(models.Model):
    classify_id = models.CharField(max_length=64,verbose_name='classify_id')
    username= models.CharField(max_length=32,verbose_name='username')
    galaxy_name = models.CharField(max_length=32,verbose_name='galaxy_name')
    created_time = models.DateTimeField(auto_now_add=True)
    last_change_time = models.DateTimeField(default=timezone.now)
    choices1=((0,'Elliptical'),(1,'Spiral'),(2,'Disk'),(3,'Stars'),(4,'Others'))
    type1=models.IntegerField(choices=choices1,verbose_name='type1',default=0,null=True)
    notation = models.TextField(max_length = 200)
