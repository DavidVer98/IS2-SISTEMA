from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from django.contrib.auth.models import Group, Permission
from proyecto.models import Proyecto, Miembro

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
        fields =  ['nombre_proyecto','scrum_master', 'fecha_inicio']

class setMiembroForms(ModelForm):
    # pk = forms.IntegerField()
    class Meta:
        model = Miembro
        fields =  ['miembro','proyectos','rol']
        # exclude = ['pk']
        exclude = ['proyectos']
class CrearGrupo(forms.Form):

    nombre = forms.CharField(max_length=50, required=True)
    permisos_proyecto = forms.MultipleChoiceField(choices=permissions, required=False)


class EditarGrupo(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    permisos_proyecto = forms.MultipleChoiceField(choices=permissions, required=False)
    rol_id = forms.CharField(widget=forms.HiddenInput())

class editar_rolmiembro_form(ModelForm):
    class Meta:
        model = Miembro
        fields =  ['rol']