from django.contrib.auth.models import Group, Permission
from django.shortcuts import render

# Create your views here.
from .forms import CrearGrupo
def crear(request):
    if request.method == "POST":
        form=CrearGrupo(request.POST or None)
        if form.is_valid():
            picked = form.cleaned_data.get('picked')
            print(picked)
            form.save()
    else:
        form = CrearGrupo()
    #grupos=Group.objects.all()
    permisos=Permission.objects.all()
    context={ 'Permisos':permisos,'form':form}
    return render(request, "rol/crear.html", context)



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
