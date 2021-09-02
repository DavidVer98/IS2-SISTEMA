from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from guardian.shortcuts import assign_perm

from proyecto.models import Proyecto

# Create your views here.
from django.contrib.auth.models import Group, Permission

from user.models import User
from .models import Rol
from proyecto.forms import ProyectoForm, ProyectoCrearForms, setMiembroForms, CrearGrupo, EditarGrupo
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
            data = form.cleaned_data
            proyecto = data['proyectos']
            user = data['miembro']
            rol = data['rol']
            print(type(rol))
            print("Proyecto ->",proyecto, "Miembro",user, "Rol",rol)
            usuario = User.objects.get(username=user)
            usuario.groups.add(rol.group)
            form.save()

    else:
        form = setMiembroForms()
        form.fields["rol"].queryset=Proyecto.objects.get(pk=proyecto_id).roles
    context = {'form': form}
    return render(request, "proyecto/setMiembro.html", context)


def crearGrupo(request, proyecto_id):
    if request.method == "POST":
        form = CrearGrupo(request.POST or None)
        if form.is_valid():

            data = form.cleaned_data
            nombre = data['nombre']
            permisos_elegidos = data['permisos_proyecto']

            if Rol.objects.filter(nombre=nombre).exists():
                # No se puede crear el rol ya que existe uno con ese nombre
                print('Un rol ya existe con ese nombre')
            else:
                # No existe un grupo con el mismo

                grupo = Group.objects.create(name=nombre)
                proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

                rol = Rol.objects.create_rol(nombre, grupo)
                proyecto_actual.roles.add(rol)

                for perm in permisos_elegidos:
                    assign_perm(perm, rol.group, proyecto_actual)

                rol.save()

    else:
        form = CrearGrupo()
    # grupos=Group.objects.all()
    permisos = Permission.objects.all()
    context = {'Permisos': permisos, 'form': form, 'proyecto_id': proyecto_id}
    return render(request, "rol/crear.html", context)


def asignarPermisos(request, miembro_id):
    miembro = Miembro.objects.get(pk=miembro_id)
    print("Miembro -->", miembro)


def listarRol(request, proyecto_id):
    roles = Proyecto.objects.get(pk=proyecto_id).roles.all()
    context = {'rol': roles, 'proyecto_id':proyecto_id}
    return render(request, "rol/listarRol.html", context)


def editarRol(request, rol_id, proyecto_id):
    print('ProyectoIDpa',proyecto_id)
    # se deben reasignar los usuarios que tengan el rol, al nuevo grupo donde estaran los nuevos permisos
    if request.method == "POST":
        form = EditarGrupo(request.POST or None)

        if form.is_valid():
            data = form.cleaned_data
            nombre = data['nombre']
            permisos_elegidos = data['permisos_proyecto']

            # No es posible editar un rol que esta asignado a algun miembro
            rol_actual = Rol.objects.get(pk=rol_id)


            # Se trae el modelo del rol

            rol_actual.nombre=nombre
            # se extraen los miembros del proyecto con el rol
            miembros_con_el_rol = Miembro.objects.filter(rol=rol_actual)

            # Se estrae el grupo del rol y se elimina
            grupo_anterior = rol_actual.group


            # se crea nuevo grupo
            rol_actual.group = Group.objects.create(name=nombre)
            #SE NECESITA EL PROYECTO_ID PARA ASIGNAR LOS NUEVOS PERMISOS
            proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

            # se asignan los nuevos permisos al grupo
            for perm in permisos_elegidos:
                assign_perm(perm, rol_actual.group, proyecto_actual)
            # se agregan a los miembros al nuevo grupo si es que alguno existe
            if miembros_con_el_rol.exists():
                for miembro in miembros_con_el_rol:
                     miembro.miembro.groups.add(rol_actual.group)


            grupo_anterior.delete()
            rol_actual.group.save()
            rol_actual.save()
            proyecto_actual.roles.add(rol_actual)
            proyecto_actual.save()
            # proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
            #
            # rol = Rol.objects.create_rol(nombre, grupo)
            # proyecto_actual.roles.add(rol)
            #
            # rol.save()
            # for perm in permisos_elegidos:
            #     assign_perm(perm, rol.group, proyecto_actual)

    else:
        form = EditarGrupo()

    context = {"rol_id": rol_id, "proyecto_id":proyecto_id ,"form": form}
    return render(request, "rol/editar.html", context)


def eliminarRol(request, rol_id, proyecto_id):
    print(rol_id)
    rol= Rol.objects.get(id=rol_id)
    print(rol)

    return redirect("/proyecto/rol/listar")


def eliminarmiembro(request, proyecto_id, miembro_id):
    miembro = Miembro.objects.get(pk=miembro_id)
    miembro.delete()
    return getMiembros(request, proyecto_id)


def eliminarProyecto(request,proyecto_id):
    print(proyecto_id)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    proyecto.delete()

    return redirect("/home/proyectos/")
