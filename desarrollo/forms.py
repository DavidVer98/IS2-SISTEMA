from desarrollo.models import UserStory, EstimacionPlanificada, RegistroUserStory
from django import forms

from proyecto.models import Proyecto, Miembro

class UserStoryForms(forms.ModelForm):
    # proyecto = forms.ForeignKey(Proyecto)
    # miembro = forms.ForeignKey(Miembro, blank=True, null=True)
    # nombre = forms.CharField(max_length=50)
    # descripcion = forms.TextField(max_length=300)
    # estado = forms.CharField(max_length=50, choices=ESTADO_USERSTORY_CHOICES, default=TO_DO)
    # estimacion = forms.FloatField()
    # prioridad = forms.IntegerField(choices=PRIORIDAD_USERSTORY_CHOICES, blank=True)
    class Meta:
        model = UserStory
        fields = ['nombre', 'descripcion', 'miembro', 'proyecto', 'miembro', 'estado_sprint', 'estimacion', 'prioridad',
                  'estado_desarrollo']
        exclude = ['proyecto', 'miembro', 'estado_sprint', 'estimacion', 'estado_desarrollo']


class UserStoryMiembroForms(forms.ModelForm):
    class Meta:
        model = UserStory
        fields = ['nombre', 'descripcion', 'miembro_asignado', 'proyecto', 'estado_sprint', 'estimacion', 'prioridad',
                  'estado_desarrollo']
        exclude = ['nombre', 'descripcion', 'proyecto', 'estado_sprint', 'estimacion', 'prioridad',
                   'estado_desarrollo']


class PlanningPokerForms(forms.ModelForm):
    class Meta:
        model= EstimacionPlanificada
        fields = ['estimacion_scrum','estimacion_miembro']

class UserStoryRegistroForms(forms.ModelForm):
    class Meta:
        model = RegistroUserStory
        fields = ['user_story', 'detalles','fecha' ,'horas_trabajadas', 'horas_totales', 'nombre_user_story']
        exclude = ['user_story', 'fecha', 'horas_totales', 'nombre_user_story']
