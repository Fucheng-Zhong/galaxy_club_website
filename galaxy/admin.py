from django.contrib import admin
from .models import Galaxies
from .models import UserClassifyRecord
# Register your models here.

admin.site.register(Galaxies)
admin.site.register(UserClassifyRecord)