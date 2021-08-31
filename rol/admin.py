from django.contrib import admin
from .models import Rol
from django.contrib.auth.models import  Permission
# Register your models here.

admin.site.register(Rol)
admin.site.register(Permission)