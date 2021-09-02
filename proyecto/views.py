from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from guardian.shortcuts import assign_perm

from proyecto.models import Proyecto

# Create your views here.
from django.contrib.auth.models import Group, Permission

from user.models import User
from .models import Rol
from proyecto.forms import ProyectoForm, ProyectoCrearForms, setMiembroForms, CrearGrupo
from proyecto.models import Proyecto, Miembro


@login_required(login_url='/login')
def listarProyectos(request):
    proyecto = Proyecto.objects.all()
    miembro = Miembro.objects.all()
    context = {'proyectos': proyecto, 'miembros': miembro}
    return render(request, "home/listarProyectos.html", context)


@login_required(login_url='/login')
def editarProyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    if request.method == "POST":
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect("listarProyectos")
    else:
        form = ProyectoForm(instance=proyecto)
    context = {"form": form}
    # print("editar ->",context)
    return render(request, "proyecto/editar.html", context)


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
    context = {'form': form}
    return render(request, "proyecto/crearProyecto.html", context)


def proyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    # print(proyecto.nombre_proyecto,proyecto.pk)
    context = {'proyecto_id': proyecto_id,
               'proyecto': proyecto}

    return render(request, "proyecto/proyecto.html", context)


def getMiembros(request, proyecto_id):
    # print(proyecto_id)
    proyect = Proyecto.objects.get(pk=proyecto_id)
    miembros_proyecto = Miembro.objects.filter(proyectos__pk=proyecto_id)
    # for i in miembros_proyecto:
    #     print(i.proyectos.pk)
    print(miembros_proyecto)
    # url = request.META['HTTP_REFERER']
    # for i in url:

    # print("url anterior ->",type(request.META['HTTP_REFERER']))
    # print("id del proyecto -> ",proyecto_id)
    # miembros_proyecto = Miembro.objects.get(proyectos = proyecto_id)
    # print(proyecto.nombre_proyecto,proyecto.pk)
    context = {'miembros_proyecto': miembros_proyecto, 'proyecto_id': proyecto_id}

    return render(request, "proyecto/miembros.html", context)


def setMiembros(request, proyecto_id):
    context = {}
    if request.method == "POST":
        form = setMiembroForms(request.POST)
        if form.is_valid():
            # print()
            data = form.cleaned_data
            proyecto = data['proyectos']
            user = data['miembro']
            rol = data['rol']
            # print("Proyecto ->",proyecto, "Miembro",user, "Rol",rol)
            usuario = User.objects.get(username=user)
            proyecto = Proyecto.objects.get(nombre_proyecto=proyecto)
            grupo = Rol.objects.get(group=rol)
            rol = Group.objects.get(name="grupoprueba25")
            print(usuario.email, "Proyecto ->", proyecto.pk, "Grupo", grupo.group)
            assign_perm('proyecto.VISUALIZAR_PROYECTOS', grupo.group, proyecto)
            usuario.groups.add(grupo.group)
            print(usuario.has_perm('proyecto.VISUALIZAR_PROYECTOS', proyecto))

            form.save()
            # return redirect("miembros_proyecto")
    else:
        form = setMiembroForms()
    context = {'form': form}
    return render(request, "proyecto/setMiembro.html", context)


def crearGrupo(request, proyecto_id):
    if request.method == "POST":
        form = CrearGrupo(request.POST or None)
        if form.is_valid():

            data = form.cleaned_data
            nombre = data['nombre']
            permisos_elegidos = data['permisos_proyecto']

            if Group.objects.filter(name=nombre).exists():
                # No se puede crear el grupo ya que existe el mismo id
                print('Un objeto grupo ya existe con ese nombre')
            else:
                # No existe un grupo con el mismo

                grupo = Group.objects.create(name=nombre)
                proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

                rol = Rol.objects.create_rol(nombre, grupo)
                rol.save()
                for perm in permisos_elegidos:
                    assign_perm(perm, rol.group, proyecto_actual)


    else:

        form = CrearGrupo()
    # grupos=Group.objects.all()
    permisos = Permission.objects.all()
    context = {'Permisos': permisos, 'form': form, 'proyecto_id': proyecto_id}
    return render(request, "rol/crear.html", context)


def asignarPermisos(request, miembro_id):
    miembro = Miembro.objects.get(pk=miembro_id)
    print("Miembro -->", miembro)
