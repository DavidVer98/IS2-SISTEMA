from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from proyecto.forms import ProyectoForm, ProyectoCrearForms
from proyecto.models import Proyecto


@login_required(login_url='/login')
def listarProyectos(request):
    proyecto = Proyecto.objects.all()
    print("proyecto ->",proyecto)
    context = {'proyectos': proyecto}
    return render(request, "home/listarProyectos.html" , context)

@login_required(login_url='/login')
def editarProyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(pk = proyecto_id)
    if request.method == "POST":
        form = ProyectoForm(request.POST, instance = proyecto)
        if form.is_valid():
            form.save()
            return redirect("listarProyectos")
    else:
        form = ProyectoForm(instance=proyecto)
    context = { "form" : form}
    print("editar ->",context)
    return render(request, "proyecto/editar.html",context)

@login_required(login_url='/login')
def crearProyecto(request):
    context = {}
    if request.method == "POST":
        form = ProyectoCrearForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarProyectos")
    else:
        form = ProyectoCrearForms()
    context = {'form' : form}
    return render (request,"proyecto/crearProyecto.html",context)