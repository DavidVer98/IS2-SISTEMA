from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect

# Create your views here.
from home.forms import UserForm, UserFormRol
from user.models import User

@login_required(login_url='/login')
def home(request):
    """
    Vista utilizada para para retornar a los usuarios activados, el menu inicial del sistema.
    03/09/21
     """
    return render(request, 'home/index.html')

@login_required(login_url='/login')
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
def eliminar(request, user_id):
    """
    Vista que permite la eliminacion de los usuarios existentes en la base de datos
    03/09/21
    """
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect("home")


@login_required(login_url='/login')
def editar(request, user_id):
    """
    Vista utilizada para retornar, validar y guardar un formulario de edicion de usuario a nivel de sistema
    03/09/21
     """
    user= User.objects.get(id=user_id)
    if request.method == "POST":
        form = UserFormRol(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserFormRol(instance=user)
    context = { "form" : form}
    return render(request, "user/editar.html", context)
