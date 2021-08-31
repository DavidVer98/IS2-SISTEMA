from django.db import models
from django.contrib.auth.models import Group, Permission
# Create your models here.

class Rol(models.Model):
    nombre=models.TextField(max_length=50)
    group=models.OneToOneField(Group,on_delete=models.CASCADE,primary_key=True)
