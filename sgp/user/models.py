from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    rolSistema = models.CharField(max_length=30, blank=True,default='Usuario')
    estaActivado = models.BooleanField(default=False)
    # def save(self, args, kwargs):
    #     if self.pk is None:
    #         self.set_password(self.password)
    #         super().save(args, kwargs)
