from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect

# Create your views here.
from home.forms import UserForm, UserFormRol
from user.models import User


def home(request):
    return render(request,'home/index.html')

@permission_required('user.view_user', login_url="/home/")
def listarUsuarios(request):
    user = User.objects.all()
    context = {'user': user}
    print(request.user.has_perm('user.view_user'))
    # print(user.hasper)
    return render(request, 'home/listaUsuarios.html', context)

def agregar(request):
    if request.method == "POST":
        form = UserForm(request.POST)   #se llena el form con los datos del usuario
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'user/agregar.html', context)

def eliminar(request, user_id):
    user= User.objects.get(id=user_id)
    user.delete()
    return redirect("home")

def editar(request, user_id):
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