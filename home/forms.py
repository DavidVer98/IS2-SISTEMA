from django.forms import *

from user.models import User


class UserFormRol(ModelForm):
    #tarea = models.CharField(max_length=100)
    class Meta:
        model = User #asosiciar un modelo a User
        fields = ['rolSistema','estaActivado']
        # widgets = {
        #     'first_name': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese sus nombres',
        #         }
        #     ),
        #     'last_name': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese sus apellidos',
        #         }
        #     ),
        #     'email': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese su email',
        #         }
        #     ),
        #     'username': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese su username',
        #         }
        #     ),
        #     'password': PasswordInput(
        #         attrs={
        #             'placeholder': 'Ingrese su password',
        #         }
        #     ),
        # }
        # exclude = ['first_name', 'last_name', 'email', 'username', 'password','groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

class UserForm(ModelForm):
    #tarea = models.CharField(max_length=100)
    class Meta:
        model = User #asosiciar un modelo a User
        fields = ['rolSistema']
        # widgets = {
        #     'first_name': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese sus nombres',
        #         }
        #     ),
        #     'last_name': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese sus apellidos',
        #         }
        #     ),
        #     'email': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese su email',
        #         }
        #     ),
        #     'username': TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese su username',
        #         }
        #     ),
        #     'password': PasswordInput(
        #         attrs={
        #             'placeholder': 'Ingrese su password',
        #         }
        #     ),
        # }
        exclude = ['first_name', 'last_name', 'email', 'username', 'password','groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']