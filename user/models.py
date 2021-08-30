from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    USUARIO= 'Usuario'
    ADMINISTRADOR = 'Administrador'
    ROL_SISTEMA_CHOICES = [
        (USUARIO, 'Usuario'),
        (ADMINISTRADOR, 'Administrador')
    ]
    rolSistema = models.CharField(max_length=30, choices=ROL_SISTEMA_CHOICES, blank=True, default="")
    estaActivado = models.BooleanField(default=False)

    # def save(self, args, kwargs):
    #     if self.pk is None:
    #         self.set_password(self.password)
    #         super().save(args, kwargs)
