from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from guardian.decorators import permission_required_or_403
from guardian.mixins import LoginRequiredMixin, PermissionListMixin
from guardian.shortcuts import assign_perm, get_group_perms
import requests

from desarrollo.models import UserStory, Sprint
from desarrollo.views import desarrollo
from proyecto.models import Proyecto

# Create your views here.
from django.contrib.auth.models import Group, Permission

from user.models import User
from .models import Rol
from proyecto.forms import ProyectoForm, ProyectoCrearForms, setMiembroForms, CrearGrupo, EditarGrupo, permissions, \
    editar_rolmiembro_form
from proyecto.models import Proyecto, Miembro


def listarProyectos(request):
    """
       Listar Proyecto:
        03/09/2021
        Vista utilizada para crear listar los proyectos
        creados en el sistema.
    """
    proyecto = Proyecto.objects.all()
    miembro = Miembro.objects.all()
    context = {'proyectos': proyecto, 'miembros': miembro}
    return render(request, "home/listarProyectos.html", context)

def filtrarProyecto(request,proyecto_estado):
    """
       filtrar Proyecto:
        13/09/2021
        Vista utilizada para filtrar los proyectos asegun su estado.
    """
    if(proyecto_estado!= "TODOS"):
        proyecto = Proyecto.objects.filter(estado=proyecto_estado)
    else:
        proyecto = Proyecto.objects.all()
    miembro = Miembro.objects.all()
    context = {'proyectos': proyecto, 'miembros': miembro, 'filtro':proyecto_estado}
    return render(request, "home/listarProyectos.html", context)

@login_required(login_url='/login')
@permission_required('user.EDITAR_PROYECTOS', login_url='/home')
def editarProyecto(request, proyecto_id):
    """
       **Editar Proyecto:**
        03/09/2021
        Vista utilizada para edtiar el proyecto .
        Solicita el id del proyecto a editar
        Requiere que el usuario este logeado

    """
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    nombre_anterior = proyecto.nombre_proyecto
    if request.method == "POST":
        form = ProyectoForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            nombre_proyecto = data['nombre_proyecto']
            descripcion = data['descripcion']
            scrum_nuevo = data['scrum_master']
            proyecto_actual = Proyecto.objects.filter(nombre_proyecto=nombre_proyecto)
            if (not proyecto_actual.exists()) or nombre_anterior == nombre_proyecto:
                proyecto.nombre_proyecto = nombre_proyecto
            proyecto.descripcion = descripcion
            proyecto.reasignarScrum(scrum_nuevo)
            return redirect("listarProyectos")
    else:
        form = ProyectoForm(instance=proyecto)
        #se filtra de la lista a los usuarios de tipo administrador
        form.fields['scrum_master'].queryset = User.objects.all().exclude(groups__name='Administrador')
    proyecto = Proyecto.objects.get(id=proyecto_id)
    context = {"form": form, 'proyecto': proyecto}

    return render(request, "proyecto/editar.html", context)


@login_required(login_url='/login')
@permission_required('user.CREAR_PROYECTO', login_url='/home')
def crearProyecto(request):
    """
       **Crear Proyecto:**
        03/09/2021
        Vista utilizada para crear el proyecto .
        Requiere que el usuario este logeado

    """
    error = False
    if request.method == "POST":
        form = ProyectoCrearForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nombre_proyecto = data['nombre_proyecto']
            proyecto_actual = Proyecto.objects.filter(nombre_proyecto=nombre_proyecto)
            if not proyecto_actual.exists():
                user = data['scrum_master']
                form.save()
                proyecto_actual = Proyecto.objects.get(nombre_proyecto=nombre_proyecto)
                #rol = Rol.crearScrum(proyecto_actual.pk)
                rol=Rol.rolespordefecto(proyecto_actual.pk)
                proyecto_actual.setScrum(user, rol)
                return redirect("listarProyectos")
            else:
                error = True

    form = ProyectoCrearForms()
    form.fields['scrum_master'].queryset= User.objects.all().exclude(groups__name='Administrador')
    context = {'error': error, 'form': form, 'proyectos': proyecto}
    return render(request, "proyecto/crearProyecto.html", context)


@permission_required_or_403('VER_PROYECTO', (Proyecto, 'id', 'proyecto_id'))
def proyecto(request, proyecto_id):
    """
       **Vista Proyecto:**
        03/09/2021
        Vista utilizada recibir a los usuarios en un proyecto.
        Solicita el id del proyecto
    """
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    try:
        miembro = Miembro.objects.get(proyectos=proyecto_id, miembro=request.user)
        if proyecto.estado == proyecto.PENDIENTE or miembro.rol.nombre =='Scrum Master':
            miembros = Miembro.objects.filter(proyectos=proyecto_id)
            proyecto = Proyecto.objects.get(pk=proyecto_id)
            roles = proyecto.roles.all()

            context = {'proyecto_id': proyecto_id, 'miembros':miembros,
                       'proyecto': proyecto, 'roles':roles, 'error':False}

            return render(request, "proyecto/proyecto.html", context)
        elif proyecto.estado != proyecto.PENDIENTE:
            return redirect(reverse('desarrollo', kwargs={'proyecto_id': proyecto_id}))


    except Exception as e:
        return redirect("listarProyectos")


@permission_required_or_403('VER_MIEMBRO', (Proyecto, 'id', 'proyecto_id'))
def getMiembros(request, proyecto_id):
    """
       **Listar Miembros :**
        03/09/2021
        Vista utilizada para listar los miembros del proyecto .
        Solicita el id del proyecto

    """
    proyect = Proyecto.objects.get(pk=proyecto_id)
    miembros_proyecto = Miembro.objects.filter(proyectos__pk=proyecto_id)
    print(miembros_proyecto)
    context = {'miembros_proyecto': miembros_proyecto, 'proyecto_id': proyecto_id, 'proyecto': proyect}

    return render(request, "proyecto/miembros.html", context)


@permission_required_or_403('AGREGAR_MIEMBRO', (Proyecto, 'id', 'proyecto_id'))
def setMiembros(request, proyecto_id):
    """
       **A??adir miembros:**
        03/09/2021
        Vista utilizada para a??adir miembros al proyecto .
        Solicita el id del proyecto
    """
    context = {'proyecto_id': proyecto_id}
    context['proyecto_id'] = proyecto_id
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    if request.method == "POST":
        form = setMiembroForms(request.POST)
        form.fields["rol"].queryset = Proyecto.objects.get(pk=proyecto_id).roles
        if form.is_valid():
            data = form.cleaned_data
            proyecto = Proyecto.objects.get(pk=proyecto_id)
            user = data['miembro']
            rol = data['rol']
            miembro = Miembro.objects.filter(miembro=user, proyectos=proyecto)
            # print(miembro.exists())
            if not miembro.exists():
                user.groups.add(rol.group)
                form.instance.proyectos = proyecto
                form.save()
            return redirect(reverse('proyecto', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = setMiembroForms()
        scrum = 'Scrum Master'
        form.fields["miembro"].queryset = User.objects.all().exclude(miembro__proyectos=proyecto).\
            exclude(groups__name='Administrador')
        form.fields["rol"].queryset = Proyecto.objects.get(pk=proyecto_id).roles.exclude(nombre=scrum)
    context = {'form': form, 'proyecto_id': proyecto.pk, 'proyecto': proyecto}
    return render(request, "proyecto/setMiembro.html", context)


@permission_required_or_403('CREAR_ROL', (Proyecto, 'id', 'proyecto_id'))
def crearGrupo(request, proyecto_id):
    """
       **Crear Grupo:**
        03/09/2021
        Vista utilizada para crear el grupo.
        Solicita el id del proyecto
    """
    if request.method == "POST":
        form = CrearGrupo(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            nombre = data['nombre']
            permisos_elegidos = data['permisos_proyecto']
            proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
            if nombre in proyecto_actual.roles.all():
                print('Un rol ya existe con ese nombre')
            else:
                # No existe un grupo con el mismo
                Rol.crear(nombre, permisos_elegidos, proyecto_actual)
            return redirect(reverse('listaRol', kwargs={'proyecto_id': proyecto_id}))
    else:

        form = CrearGrupo()
    proyecto = Proyecto.objects.get(pk=proyecto_id)

    context = {'form': form, 'proyecto_id': proyecto_id, 'proyecto': proyecto}
    return render(request, "rol/crear.html", context)


@permission_required_or_403('VER_ROL', (Proyecto, 'id', 'proyecto_id'))
def listarRol(request, proyecto_id):
    """
       **Listar Roles:**
        03/09/2021
        Vista utilizada para listar los roles del sistema .
        Solicita el id del proyecto

    """
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    roles = proyecto.roles.all()
    context = {'rol': roles, 'proyecto_id': proyecto_id, 'proyecto': proyecto}
    return render(request, "rol/listarRol.html", context)


@permission_required_or_403('EDITAR_ROL', (Proyecto, 'id', 'proyecto_id'))
def editarRol(request, rol_id, proyecto_id):
    """
       **Editar Rol:**
        03/09/2021|
        Vista utilizada para edtiar el rol de los miembros de los proyectos .
        Solicita el id del proyecto
    """
    proyecto_actual = Proyecto.objects.get(id=proyecto_id)
    if request.method == "POST":
        form = EditarGrupo(request.POST or None)

        if form.is_valid():
            data = form.cleaned_data
            # nombre = data['nombre']
            permisos_elegidos = data['permisos_proyecto']

            rol_actual = Rol.objects.get(pk=rol_id)
            rol_actual.editar(permisos_elegidos, proyecto_id)

            return redirect(reverse('listaRol', kwargs={'proyecto_id': proyecto_id}))

    else:
        rol_actual = Rol.objects.get(pk=rol_id)
        print(rol_actual.nombre)
        form = EditarGrupo()

    rol_nombre = Rol.objects.get(id=rol_id)
    context = {"rol_id": rol_id, "proyecto_id": proyecto_id, "form": form, 'proyecto': proyecto_actual,
               'rol_nombre': rol_nombre}
    return render(request, "rol/editar.html", context)


@permission_required_or_403('ELIMINAR_ROL', (Proyecto, 'id', 'proyecto_id'))
def eliminarRol(request, rol_id, proyecto_id):
    """
       **Eliminar Rol:**
        03/09/2021
        Vista utilizada para eliminar los roles de un proyecto.
        Solicita el id del proyecto y la id del rol
    """
    rol = Rol.objects.get(id=rol_id)
    error = False
    if not Miembro.objects.filter(rol=rol).exists():  # validar eliminacion de rol
        grupo = rol.group
        grupo.delete()
        rol.delete()
    else:
        error = True
    return redirect(reverse("listaRol", kwargs={"proyecto_id": proyecto_id}))


@permission_required_or_403('ELIMINAR_MIEMBRO', (Proyecto, 'id', 'proyecto_id'))
def eliminarmiembro(request, proyecto_id, miembro_id):
    """
       **Eliminar Miembro:**
        03/09/2021
        Vista utilizada para elimianr miembros del proyecto .
        Solicita el id del proyecto y el id de los miembro
    """
    miembro = Miembro.objects.get(pk=miembro_id)
    usuario = miembro.miembro
    miembro_en_sprint_activo=UserStory.objects.filter(proyecto__id=proyecto_id, estado_desarrollo=UserStory.EN_SPRINT_BACKLOG, miembro_asignado=usuario)
    if miembro.rol.nombre != 'Scrum Master' and not miembro_en_sprint_activo.exists():
        usuario.groups.remove(miembro.rol.group)
        user_stories=UserStory.objects.filter(proyecto__id=proyecto_id, estado_desarrollo=UserStory.EN_SPRINT_PLANNING, miembro_asignado=usuario)
        for user_story in user_stories:
            user_story.miembro_asignado=None
            user_story.save()
        miembro.delete()
    return redirect(reverse('miembros_proyecto', kwargs={'proyecto_id': proyecto_id}))


@permission_required_or_403('EDITAR_MIEMBRO', (Proyecto, 'id', 'proyecto_id'))
def editar_rolmiembro(request, proyecto_id, miembro_id):
    """
       **Editar Roles de los mimebros de un proyecto:**
        03/09/2021
        Vista utilizada para edtiar los roles de los miembros de un proyecto.
    """
    miembro = Miembro.objects.get(pk=miembro_id)

    if request.method == "POST":
        form = editar_rolmiembro_form(request.POST or None, instance=miembro)
        # form.fields["rol"].queryset = Proyecto.objects.get(pk=proyecto_id).roles
        if form.is_valid():
            miembro = Miembro.objects.get(pk=miembro_id)
            data = form.cleaned_data
            rol = data['rol']
            usuario = miembro.miembro
            rol_anterior = miembro.rol.group
            usuario.groups.remove(rol_anterior)
            usuario.groups.add(rol.group)
            form.save()
            return redirect(reverse('miembros_proyecto', kwargs={'proyecto_id': proyecto_id}))

    else:
        form = editar_rolmiembro_form(instance=miembro)
        scrum = 'Scrum Master'
        form.fields["rol"].queryset = Proyecto.objects.get(pk=proyecto_id).roles.exclude(nombre=scrum)
        miembro_nombre = Miembro.objects.get(id=miembro_id)

    proyect = Proyecto.objects.get(pk=proyecto_id)
    miembros_proyecto = Miembro.objects.filter(proyectos__pk=proyecto_id)

    context = {"proyecto_id": proyecto_id, "miembro_id": miembro_id, "form": form, 'miembro_nombre': miembro_nombre,
               'miembros_proyecto': miembros_proyecto, 'proyecto': proyect}
    return render(request, "proyecto/miembroEditar.html", context)


@permission_required_or_403('CANCELAR_PROYECTO', (Proyecto, 'id', 'proyecto_id'))
def cancelarProyecto(request, proyecto_id):
    """
       **Cancelar Proyecto:**
        03/09/2021
        Vista utilizada para cancelar un proyecto.
        Solicita el id del proyecto
    """

    proyecto = Proyecto.objects.get(id=proyecto_id)
    if proyecto.estado != proyecto.CANCELADO:
        proyecto.estado = proyecto.CANCELADO

        miembros_proyecto = Miembro.objects.filter(proyectos__pk=proyecto_id)
        rol_solo_visualizacion = Rol.objects.get(group__name='Product Owner'+str(proyecto_id))

        for miembro in miembros_proyecto.all():
            miembro.miembro.groups.remove(miembro.rol.group)
            miembro.miembro.groups.add(rol_solo_visualizacion.group)

        proyecto.save()


    return redirect("/home/proyectos/")

@login_required(login_url='/login')
@permission_required('user.BORRAR_PROYECTO', login_url='/home')
def BorrarProyecto(request, proyecto_id):
    """
       **Cancelar Proyecto:**
        03/09/2021
        Vista utilizada para cancelar un proyecto.
        Solicita el id del proyecto
    """

    proyecto = Proyecto.objects.get(id=proyecto_id)
    if proyecto.estado == proyecto.PENDIENTE:
        proyecto.delete()

    return redirect("/home/proyectos/")


@permission_required_or_403('INICIAR_PROYECTO', (Proyecto, 'id', 'proyecto_id'))
def iniciar_proyecto(request, proyecto_id):
    """
       **Iniciar Proyecto:**
        03/09/2021
        Vista utilizada para iniciar el proyecto .
        Solicita el id del proyecto
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    proyecto_actual.iniciar_proyecto()
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual}
    return redirect(reverse('desarrollo', kwargs={'proyecto_id': proyecto_id}))

@permission_required_or_403('VER_ROL', (Proyecto, 'id', 'proyecto_id'))
def permisosRol(request, rol_id, proyecto_id):
    """
       **Iniciar Proyecto:**
        08/09/2021
        Vista utilizada para listar los permisos de un rol .
        Solicita el id del proyecto
    """
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    rol_actual = Rol.objects.get(pk=rol_id)
    permisos_rol = get_group_perms(rol_actual.group, proyecto)
    nombre_rol = rol_actual.nombre
    nombre_permiso = Permission.objects.filter(codename__in=permisos_rol).values('name')

    context = {'permisos_rol': nombre_permiso, 'proyecto_id': proyecto_id, 'proyecto': proyecto ,'nombre_rol':nombre_rol}
    return render(request, "rol/listarPermisos.html", context)

@permission_required_or_403('CANCELAR_PROYECTO', (Proyecto, 'id', 'proyecto_id'))
def terminarProyecto(request, proyecto_id):
    """
       **Terminar Proyecto:**
        18/11/2021
        Vista utilizada para Terminar un proyecto.
        Solicita el id del proyecto
    """

    proyecto = Proyecto.objects.get(id=proyecto_id)

    if proyecto.estado != proyecto.CANCELADO or proyecto.estado != proyecto.FINALIZADO :
        xd= Sprint.objects.filter(proyecto=proyecto, estado=Sprint.ACTIVO)
        if not xd.exists():
            proyecto.estado = proyecto.FINALIZADO

            miembros_proyecto = Miembro.objects.filter(proyectos__pk=proyecto_id)
            rol_solo_visualizacion = Rol.objects.get(group__name='Product Owner'+str(proyecto_id))

            for miembro in miembros_proyecto.all():
                miembro.miembro.groups.remove(miembro.rol.group)
                miembro.miembro.groups.add(rol_solo_visualizacion.group)

            proyecto.save()
        else:
            try:

                miembro = Miembro.objects.get(proyectos=proyecto_id, miembro=request.user)
                if proyecto.estado == proyecto.PENDIENTE or miembro.rol.nombre == 'Scrum Master':
                    miembros = Miembro.objects.filter(proyectos=proyecto_id)
                    proyecto = Proyecto.objects.get(pk=proyecto_id)
                    roles = proyecto.roles.all()

                    context = {'proyecto_id': proyecto_id, 'miembros': miembros,
                               'proyecto': proyecto, 'roles': roles, 'error':True}

                    return render(request, "proyecto/proyecto.html", context)
            except Exception as e:
                return redirect("listarProyectos")

    return redirect("/home/proyectos/")