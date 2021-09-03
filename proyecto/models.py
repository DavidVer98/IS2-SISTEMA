from django.db import models
from django.contrib.auth.models import Group

from user.models import User


class RolManager(models.Manager):
    def create_rol(self, name, grupo):
        rol = self.create(nombre=name, group=grupo)
        return rol


class Rol(models.Model):
    """
    **Rol:**
    03/09/2021
    Modelo de Rol que maneja el nombre del rol y enlaza con el groups de django

    """
    nombre = models.TextField(max_length=50)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    objects = RolManager()

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    """
     **Proyecto:**
     03/09/2021
     Model de los datos necesarios para el manejo de un Proyecto

    """
    nombre_proyecto = models.CharField(max_length=50)
    scrum_master = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, default="PENDIENTE")
    fecha_inicio = models.DateField()
    roles = models.ManyToManyField(Rol)

    def __str__(self):
        return self.nombre_proyecto

    class Meta:
        permissions = [
            ("VISUALIZAR_PROYECTOS", "Puede visualizar los proyectos creados"),
            ("CREAR_PROYECTOS", "Puede crear proyectos"),
            ("CAMBIAR_ESTADO_PROYECTO", "Puede cambiar el estado de proyectos"),
            ("ELIMINAR_PROYECTOS", "Puede elimiar proyectos"),
            ("AGREGAR_MIEMBRO", "Puede agregar miembros a un proyecto"),
            ("ELIMINAR_MIEMBRO", "Puede eliminar miembros de un proyecto"),
            ("VISUALIZAR_ROLES", "Puede ver la lista de roles del proyecto"),
            ("CREAR_ROL", "Puede ver la lista de roles del proyecto"),
            ("ASIGNAR_ROL", "Puede asignar rol a un miembro de proyecto"),
        ]


class Miembro(models.Model):
    """
        **Miembro:**
        03/09/2021
        Model que representa la relacion de un usuario, un proyecto y un rol

    """
    miembro = models.ForeignKey(User, on_delete=models.PROTECT)
    proyectos = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    def __str__(self):
        return self.miembro.username
