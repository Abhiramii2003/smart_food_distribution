from django.contrib import admin
from .models import Restaurant, SurplusFood

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(SurplusFood)