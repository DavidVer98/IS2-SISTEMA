from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from django.contrib.auth.models import Group, Permission
from proyecto.models import Proyecto, Miembro



permissions = [
    ("VER_PROYECTO", "Puede visualizar el proyecto en la lista de proyectos"),
    ("CREAR_PROYECTO", "Puede crear proyectos"),
    ("EDITAR_PROYECTO", "Puede editar configuraciones basicas del proyecto"),
    ("INICIAR_PROYECTO", "Puede iniciar la ejecucion de un proyecto"),
    ("ELIMINAR_PROYECTO", "Puede eliminar el proyecto"),
    ("VER_MIEMBRO", "Puede ver la lista de miembros del proyecto"),
    ("AGREGAR_MIEMBRO", "Puede agregar miembros al proyecto"),
    ("EDITAR_MIEMBRO", "Puede editar roles de miembros del proyecto"),
    ("ELIMINAR_MIEMBRO", "Puede eliminar miembros del proyecto"),
    ("VER_ROL", "Puede ver lista de roles del proyecto"),
    ("CREAR_ROL", "Puede crear roles del proyecto"),
    ("EDITAR_ROL", "Puede editar roles del proyecto"),
    ("ELIMINAR_ROL", "Puede eliminar roles del proyecto"),
]


class ProyectoForm(ModelForm):
    # tarea = models.CharField(max_length=100)
    class Meta:
        model = Proyecto  # asosiciar un modelo a Proyecto
        fields = ['nombre_proyecto', 'scrum_master', 'estado', 'fecha_inicio']
        widgets = {
            'fecha_inicio': DatePickerInput(format='%Y-%m-%d'),  # specify date-frmat
            "locale": "es",
        }

        # widgets = {
        #     'first_name': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese sus nombres',
        #         }
        # exclude = ['first_name', 'last_name', 'email', 'username', 'password','groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']


class ProyectoCrearForms(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto', 'scrum_master', 'fecha_inicio']
        widgets = {
            'fecha_inicio': DatePickerInput(format='%Y-%m-%d'),  # specify date-frmat
            "locale": "es",
        }


class setMiembroForms(ModelForm):
    # pk = forms.IntegerField()
    class Meta:
        model = Miembro
        fields = ['miembro', 'proyectos', 'rol']
        # exclude = ['pk']
        exclude = ['proyectos']


class CrearGrupo(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    permisos_proyecto = forms.MultipleChoiceField(choices=permissions, required=False)


class EditarGrupo(forms.Form):
    # nombre = forms.CharField(max_length=50, required=True)
    permisos_proyecto = forms.MultipleChoiceField(choices=permissions, required=False)
    rol_id = forms.CharField(widget=forms.HiddenInput())


class editar_rolmiembro_form(ModelForm):
    class Meta:
        model = Miembro
        fields = ['rol']
