from django.forms import ModelForm

from proyecto.models import Proyecto


class ProyectoForm(ModelForm):
    #tarea = models.CharField(max_length=100)
    class Meta:
        model = Proyecto #asosiciar un modelo a Proyecto
        fields = ['nombre_proyecto','scrum_master','estado', 'fecha_inicio']
        # widgets = {
        #     'first_name': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese sus nombres',
        #         }
        # exclude = ['first_name', 'last_name', 'email', 'username', 'password','groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']
class ProyectoCrearForms(ModelForm):
    class Meta:
        model = Proyecto
        fields =  ['nombre_proyecto','scrum_master','estado', 'fecha_inicio']