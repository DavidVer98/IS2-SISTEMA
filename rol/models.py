from django.db import models
from django.contrib.auth.models import Group, Permission
# Create your models here.

class RolManager(models.Manager):
    def create_rol(self,name, grupo):
        rol=self.create(nombre=name, group=grupo)
        return rol

class Rol(models.Model):
    nombre=models.TextField(max_length=50)
    group=models.OneToOneField(Group,on_delete=models.CASCADE,primary_key=True)
    objects= RolManager()
