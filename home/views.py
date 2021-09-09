from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from home.forms import UserForm, UserFormRol
from proyecto.models import Miembro
from user.models import User


@login_required(login_url='/login')
def home(request):
    """
    Vista utilizada para para retornar a los usuarios activados, el menu inicial del sistema.
    03/09/21
     """
    return render(request, 'home/index.html')


@login_required(login_url='/login')
@permission_required('user.VER_USUARIOS', login_url='/home')
def listarUsuarios(request):
    """
    Vista utilizada para retornar la lista de los usuarios existentes en el sistema
    03/09/21
    """
    user = User.objects.all()
    context = {'user': user}
    print(request.user.has_perm('user.view_user'))
    print(user.values())
    return render(request, 'home/listaUsuarios.html', context)


# def agregar(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)   #se llena el form con los datos del usuario
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = UserForm()
#     context = {'form': form}
#     return render(request, 'user/agregar.html', context)

@login_required(login_url='/login')
@permission_required('user.ELIMINAR_USUARIO', login_url='/home')
def eliminar(request, user_id):
    """
    Vista que permite la eliminacion de los usuarios existentes en la base de datos
    03/09/21
    """

    error=False
    usuario = User.objects.get(pk=user_id)
    if not Miembro.objects.filter(miembro=usuario).exists():
        try:
            user = User.objects.get(id=user_id)
            user.delete()
        except Exception as e:
            print(e)
    else:
        error=True
    return redirect("listaUsuarios")


@login_required(login_url='/login')
@permission_required('user.EDITAR_USUARIO', login_url='/home')
def editar(request, user_id):
    """
    Vista utilizada para retornar, validar y guardar un formulario de edicion de usuario a nivel de sistema
    03/09/21
     """
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = UserFormRol(request.POST, instance=user)
        if form.is_valid():
            form.save()

            data = form.cleaned_data
            rol_sistema = data['rolSistema']
            user = User.objects.get(pk=user_id)
            grupo_administracion = Group.objects.get(name=user.ADMINISTRADOR)
            if rol_sistema == grupo_administracion.name:
                user.groups.add(grupo_administracion)
                # user.is_superuser=True
            else:
                user.groups.remove(grupo_administracion)
                user.is_superuser = False
            user.save()
            return redirect("listaUsuarios")
    else:
        form = UserFormRol(instance=user)
    context = {"form": form, 'rol_sistema': user}
    return render(request, "user/editar.html", context)
