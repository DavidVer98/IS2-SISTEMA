from django.db import models

# Create your models here.
from proyecto.models import Proyecto, Miembro
from user.models import User


class UserStory(models.Model):

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
    BAJA = 0
    NORMAL = 1
    ALTA = 2
    PRIORIDAD_USERSTORY_CHOICES = (
        (BAJA, 'Baja'),
        (NORMAL, 'Normal'),
        (ALTA, 'Alta'),
    )


    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    miembro = models.ForeignKey(Miembro,  on_delete=models.PROTECT,blank=True, null=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=300)
    estado = models.CharField(max_length=50, choices=ESTADO_USERSTORY_CHOICES, default=TO_DO)
    estimacion = models.FloatField()
    prioridad = models.IntegerField(choices=PRIORIDAD_USERSTORY_CHOICES, blank=True)


class EstimacionPlanificada(models.Model):
    estimacion_Scrum = models.IntegerField()
    estimacion_Miembro = models.IntegerField()


class ProductBacklog(models.Model):
    userStories = models.ManyToManyField(UserStory)








