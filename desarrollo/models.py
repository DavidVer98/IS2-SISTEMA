from datetime import datetime

from django.db import models

# Create your models here.
from proyecto.models import Proyecto, Miembro
from user.models import User


class UserStory(models.Model):
    """
        **User Story:**
        03/09/2021
        Se define en la base de datos la clase de user story
        con sus respectivos atributos.

    """
    TO_DO='TO DO'
    DOING='DOING'
    DONE='DONE'
    QA = 'QA'
    RELASE = 'RELASE'

    ESTADO_USERSTORY_CHOICES = [
        ('TO DO', 'TO DO'),
        ('DOING', 'DOING'),
        ('DONE', 'DONE'),
        ('QA', 'QA'),
        ('RELEASE', 'RELEASE'),
    ]
    BAJA = 1
    NORMAL = 2
    ALTA = 3
    SUPERALTA=4
    PRIORIDAD_USERSTORY_CHOICES = (
        (BAJA, 'Baja'),
        (NORMAL, 'Normal'),
        (ALTA, 'Alta'),
        (SUPERALTA, 'Super Alta'),
    )

    class Meta:
        ordering = ["-prioridad"]


    EN_PRODUCT_BACKLOG = 'EN PRODUCT BACKLOG'
    EN_SPRINT_BACKLOG='EN SPRINT BACKLOG'
    EN_SPRINT_PLANNING='EN SPRINT PLANNING'

    ESTADO_DESARROLLO_USERSTORY_CHOICES = [
        ( EN_PRODUCT_BACKLOG, 'EN PRODUCT BACKLOG'),
        (EN_SPRINT_BACKLOG, 'EN SPRINT BACKLOG'),
        (EN_SPRINT_PLANNING, 'EN SPRINT PLANNING'),
    ]



    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    miembro_asignado = models.ForeignKey(User,  on_delete=models.PROTECT,blank=True, null=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=300)
    estado_sprint = models.CharField(max_length=50, choices=ESTADO_USERSTORY_CHOICES, default=TO_DO)
    estimacion = models.FloatField(default=0, blank=True, null=False)
    prioridad = models.IntegerField(default=BAJA, choices=PRIORIDAD_USERSTORY_CHOICES)
    estado_desarrollo = models.CharField(max_length=50,default=EN_PRODUCT_BACKLOG, choices=ESTADO_DESARROLLO_USERSTORY_CHOICES)


class EstimacionPlanificada(models.Model):
    """
        **Estimacion:**
        03/09/2021
        Se define en la base de datos la clase de estimacion
        para guardar la estimacion del scrum master como del miembro asignado.

    """
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    estimacion_scrum = models.PositiveIntegerField(default=0,blank=True, null=True)
    estimacion_miembro = models.PositiveIntegerField(default=0, blank=True, null=True)


class RegistroUserStory(models.Model):
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    detalles = models.TextField(max_length=50)
    fecha = models.DateField(default=datetime.now, blank=True)
    horas_trabajadas = models.PositiveIntegerField(default=0,blank=True, null=True)
    horas_totales = models.PositiveIntegerField(default=0, blank=True, null=True)
    contador_registro = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.user_story.nombre

# class ProductBacklog(models.Model):
#     userStories = models.ManyToManyField(UserStory)
#
#
# class SprintPlanning(models.Model):
#     userStories = models.ManyToManyField(UserStory)
#     miembros = models.ManyToManyField(Miembro)
#


class Sprint(models.Model):

    ACTIVO = 'Activo'
    FINALIZADO = 'Finalizado'

    ESTADO_CHOICES = [
        ( ACTIVO, 'Activo'),
        ( FINALIZADO, 'Finalizado'),
    ]
    nombre = models.CharField(max_length=50)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default=ACTIVO)
    fecha_inicio = models.DateField(default=datetime.now, blank=True)
    fecha_fin = models.DateField(blank=True, null=True)
    user_stories = models.ManyToManyField(UserStory)

