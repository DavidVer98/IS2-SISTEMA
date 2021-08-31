from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple, ModelChoiceField
from django.contrib.auth.models import Group, Permission
from .models import Rol

class CrearGrupo(ModelForm):
    #tarea = models.CharField(max_length=100)
    class Meta:
        model = Group
        fields = ['name','permissions']
        # widgets = {
        #     'first_name': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese sus nombres',
        #         }
        # exclude = ['first_name', 'last_name', 'email', 'username', 'password','groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']
