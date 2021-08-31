from django.contrib.auth.models import Group, Permission
from django.shortcuts import render
from .models import Rol
# Create your views here.
from .forms import CrearGrupo
def crearGrupo(request):
    if request.method == "POST":
        form=CrearGrupo(request.POST or None)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['name']
            grupos = Group.objects.all()
            for i in grupos:
                if (i.name == name):
                    Rol.objects.create_rol(name,i)

    else:
        form = CrearGrupo()
    #grupos=Group.objects.all()
    permisos=Permission.objects.all()
    context={ 'Permisos':permisos,'form':form}
    return render(request, "rol/crear.html", context)

#def crearRol(request):


    # if request.method == "POST":
    #     form = ProyectoForm(request.POST, instance = proyecto)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("listarProyectos")
    # else:
    #     form = ProyectoForm(instance=proyecto)
    # context = { "form" : form}
    # print("editar ->",context)
    # return render(request, "proyecto/editar.html",context)
