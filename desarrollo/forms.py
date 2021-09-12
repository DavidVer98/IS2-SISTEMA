from desarrollo.models import UserStory
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
        fields = ['nombre','descripcion','miembro' ,'proyecto','miembro','estado','estimacion', 'prioridad']
        exclude = ['proyecto','miembro','estado', 'estimacion']