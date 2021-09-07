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

    class Meta:
        default_permissions = ()
        permissions = [
            ("CREAR_PROYECTO", "Puede crear proyectos"),
            ("EDITAR_USUARIO", "Puede editar las opciones de sistema de los usuarios"),
            ("ELIMINAR_USUARIO", "Puede eliminar el registro de usuarios"),
            ("VER_USUARIOS", "Puede ver la lista de usuarios en el sistema"),
        ]
    # def save(self, args, kwargs):
    #     if self.pk is None:
    #         self.set_password(self.password)
    #         super().save(args, kwargs)
