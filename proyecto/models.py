
from django.db import models
from user.models import User


class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=50)
    scrum_master = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, default="PENDIENTE")
    fecha_inicio = models.DateField()


    # class Meta:
    #     permissions = [
    #         ("VISUALIZAR_PROYECTOS", "Puede visualizar los proyectos creados"),
    #         ("CREAR_PROYECTOS", "Puede crear proyectos"),
    #         ("CAMBIAR_ESTADO_PROYECTO", "Puede cambiar el estado de proyectos"),
    #         ("ELIMINAR_PROYECTOS", "Puede elimiar proyectos"),
    #         ("AGREGAR_MIEMBRO", "Puede agregar miembros a un proyecto"),
    #         ("ELIMINAR_MIEMBRO", "Puede eliminar miembros de un proyecto"),
    #         ("VISUALIZAR_ROLES", "Puede ver la lista de roles del proyecto"),
    #         ("CREAR_ROL", "Puede ver la lista de roles del proyecto"),
    #         ("ASIGNAR_ROL", "Puede asignar rol a un miembro de proyecto"),
    #     ]

