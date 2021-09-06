from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from guardian.mixins import LoginRequiredMixin, PermissionListMixin
from guardian.shortcuts import assign_perm
import requests

from proyecto.models import Proyecto

# Create your views here.
from django.contrib.auth.models import Group, Permission

from user.models import User
from .models import Rol
from proyecto.forms import ProyectoForm, ProyectoCrearForms, setMiembroForms, CrearGrupo, EditarGrupo, permissions, \
    editar_rolmiembro_form
from proyecto.models import Proyecto, Miembro


class listarProyectos(LoginRequiredMixin, PermissionListMixin, ListView):
    """
       **Listar Proyecto:**
        03/09/2021
        Vista utilizada para crear listar los proyectos
        creados en el sistema, el usuario debe tener el permiso de ver el proyecto.
    """
    model = Proyecto
    permission_required = "VER_PROYECTO"
    template_name = "home/listarProyectos.html"


@login_required(login_url='/login')
def editarProyecto(request, proyecto_id):
    """
       **Editar Proyecto:**
        03/09/2021
        Vista utilizada para edtiar el proyecto .
        Solicita el id del proyecto a editar
        Requiere que el usuario este logeado

    """
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    if request.method == "POST":
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect("listarProyectos")
    else:
        form = ProyectoForm(instance=proyecto)
    proyecto = Proyecto.objects.get(id = proyecto_id)
    context = {"form": form, 'proyecto':proyecto}
    # print("editar ->",context)
    return render(request, "proyecto/editar.html", context)

def setScrum(request, proyecto, user, rol):
    """
       **Añadir Srum Master:**
        03/09/2021
        Funcion utilizada para añadir el scrum Master al proyecto .
        Solicita el proyecto, user y el rol para añadir al proyecto

    """
    if (request.method == 'POST'):
        formMiembro = setMiembroForms(request.POST)
        formMiembro.instance.proyectos = proyecto
        formMiembro.instance.miembro = user
        formMiembro.instance.rol = rol
        formMiembro.instance.save()
        user.groups.add(rol.group)
    else:
        formMiembro = setMiembroForms()

def scrumRol(proyecto_id):
    """
       **Añadir el rol al Scrum Master:**
        03/09/2021
        Funcion utilizada para añadir el rol al Scrum Master .
        Solicita el id del proyecto, para luego crear el rol mediante
        el concatenacion del id del proyecto y luego añadirle al mismo
    """
    grupo = Group.objects.create(name='Scrum' + str(proyecto_id))
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    rol = Rol.objects.create_rol('Scrum' + str(proyecto_id), grupo)
    rol.save()
    for perm in permissions:
        assign_perm(perm[0], rol.group, proyecto_actual)
    proyecto_actual.roles.add(rol)
    return (rol)

@login_required(login_url='/login')
def crearProyecto(request):
    """
       **Crear Proyecto:**
        03/09/2021
        Vista utilizada para crear el proyecto .
        Requiere que el usuario este logeado

    """
    proyecto = Proyecto.objects.all()
    miembro = Miembro.objects.all()
    # context = {}
    if request.method == "POST":
        form = ProyectoCrearForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nombre_proyecto = data['nombre_proyecto']
            proyecto = Proyecto.objects.filter(nombre_proyecto =nombre_proyecto)
            if not proyecto.exists():
                data = form.cleaned_data
                nombre = data['nombre_proyecto']
                user = data['scrum_master']
                form.save()
                proyecto = Proyecto.objects.get(nombre_proyecto=nombre)
                rol = scrumRol(proyecto.pk)
                setScrum(request, proyecto, user, rol)
                return redirect("listarProyectos")

                context = {'proyectos': proyecto, 'miembros': miembro}
                return render(request, "listarProyectos", context)
            else:
                error = True
                context = {'error': error, 'form': form, 'proyectos': proyecto, 'miembros': miembro}
                return render(request, "proyecto/crearProyecto.html", context)

    else:
        form = ProyectoCrearForms()
    context = {'form': form}
    return render(request, "proyecto/crearProyecto.html", context)


def proyecto(request, proyecto_id):
    """
       **Vista Proyecto:**
        03/09/2021
        Vista utilizada recibir a los usuarios en un proyecto.
        Solicita el id del proyecto
    """

    proyecto = Proyecto.objects.get(pk=proyecto_id)
    try:
        miembro= Miembro.objects.get(proyectos=proyecto_id, miembro=request.user)
        scrum = 'Scrum' + str(proyecto_id)
        es_scrum=False
        if miembro.rol.nombre == scrum:
            es_scrum=True

        # print(proyecto.nombre_proyecto,proyecto.pk)
        context = {'proyecto_id': proyecto_id,
                   'proyecto': proyecto,'es_scrum':es_scrum}

        return render(request, "proyecto/proyecto.html", context)

    except Exception as e:
        return redirect("listarProyectos")


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
    context = {'miembros_proyecto': miembros_proyecto, 'proyecto_id': proyecto_id, 'proyecto':proyect}

    return render(request, "proyecto/miembros.html", context)


def setMiembros(request, proyecto_id):
    """
       **Añadir miembros:**
        03/09/2021
        Vista utilizada para añadir miembros al proyecto .
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
        scrum= 'Scrum'+ str(proyecto_id)
        form.fields["rol"].queryset=Proyecto.objects.get(pk=proyecto_id).roles.exclude(nombre=scrum)
    context = {'form': form , 'proyecto_id':proyecto.pk, 'proyecto':proyecto}
    return render(request, "proyecto/setMiembro.html", context)


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
            return redirect(reverse('listaRol', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = CrearGrupo()
    # grupos=Group.objects.all()
    proyecto = Proyecto.objects.get(pk = proyecto_id)
    permisos = Permission.objects.all()
    context = {'Permisos': permisos, 'form': form, 'proyecto_id': proyecto_id , 'proyecto': proyecto}
    return render(request, "rol/crear.html", context)


def asignarPermisos(request, miembro_id):
    """
       **Asinga Permiso:**
        03/09/2021
        Funcion utilizada para adingar permisos a los miembros del proyecto.
        Solicita el id del miembro
    """
    miembro = Miembro.objects.get(pk=miembro_id)
    # print("Miembro -->", miembro)


def listarRol(request, proyecto_id):
    """
       **Listar Roles:**
        03/09/2021
        Vista utilizada para listar los roles del sistema .
        Solicita el id del proyecto

    """
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    roles = proyecto.roles.all()
    context = {'rol': roles, 'proyecto_id':proyecto_id, 'proyecto':proyecto}
    return render(request, "rol/listarRol.html", context)



def editarRol(request, rol_id, proyecto_id):
    """
       **Editar Rol:**
        03/09/2021
        Vista utilizada para edtiar el rol de los miembros de los proyectos .
        Solicita el id del proyecto
    """
    # se deben reasignar los usuarios que tengan el rol, al nuevo grupo donde estaran los nuevos permisos
    if request.method == "POST":
        form = EditarGrupo(request.POST or None)

        if form.is_valid():
            data = form.cleaned_data
            nombre = data['nombre']
            permisos_elegidos = data['permisos_proyecto']


            rol_actual = Rol.objects.get(pk=rol_id)


            # Se trae el modelo del rol

            rol_actual.nombre=nombre
            # se extraen los miembros del proyecto con el rol
            miembros_con_el_rol = Miembro.objects.filter(rol=rol_actual)

            # Se estrae el grupo del rol y se elimina
            grupo_anterior = rol_actual.group
            grupo_anterior.delete()

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


            rol_actual.group.save()
            rol_actual.save()
            proyecto_actual.roles.add(rol_actual)
            proyecto_actual.save()
            return redirect(reverse('listaRol', kwargs={'proyecto_id': proyecto_id}))
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
        proyecto = Proyecto.objects.get(id=proyecto_id)
        rol_nombre = Rol.objects.get(id=rol_id)
    context = {"rol_id": rol_id, "proyecto_id":proyecto_id ,"form": form, 'proyecto':proyecto, 'rol_nombre':rol_nombre}

    return render(request, "rol/editar.html", context)


def eliminarRol(request, rol_id, proyecto_id):
    """
       **Eliminar Rol:**
        03/09/2021
        Vista utilizada para eliminar los roles de un proyecto.
        Solicita el id del proyecto y la id del rol
    """
    rol= Rol.objects.get(id=rol_id)
    error=False
    if not(Miembro.objects.filter(rol=rol).exists()): # validar eliminacion de rol
        grupo= rol.group
        grupo.delete()
        rol.delete()
    else:
        error = True

    return redirect(reverse("listaRol",kwargs={"proyecto_id":proyecto_id}))


def eliminarmiembro(request, proyecto_id, miembro_id):
    """
       **Eliminar Miembro:**
        03/09/2021
        Vista utilizada para elimianr miembros del proyecto .
        Solicita el id del proyecto y el id de los miembro
    """
    miembro = Miembro.objects.get(pk=miembro_id)
    usuario = miembro.miembro
    usuario.groups.remove(miembro.rol.group)
    miembro.delete()
    return getMiembros(request, proyecto_id)

def editar_rolmiembro(request, proyecto_id, miembro_id):
    """
       **Editar Roles de los mimebros de un proyecto:**
        03/09/2021
        Vista utilizada para edtiar los roles de los miembros de un proyecto.
    """
    miembro = Miembro.objects.get(pk=miembro_id)

    if request.method == "POST":
        form = editar_rolmiembro_form(request.POST or None, instance=miembro)
        form.fields["rol"].queryset = Proyecto.objects.get(pk=proyecto_id).roles
        if form.is_valid():
            data = form.cleaned_data
            rol = data['rol']
            usuario=miembro.miembro
            rol_anterior=miembro.rol.group
            usuario.groups.remove(rol_anterior)
            usuario.groups.add(rol.group)
            form.instance.save()
            return redirect(reverse('miembros_proyecto', kwargs={'proyecto_id': proyecto_id}))

    else:
        form=editar_rolmiembro_form(instance=miembro)
        form.fields["rol"].queryset = Proyecto.objects.get(pk=proyecto_id).roles
        miembro_nombre = Miembro.objects.get(id =miembro_id)

    context = {"proyecto_id": proyecto_id, "miembro_id": miembro_id, "form": form, 'miembro_nombre': miembro_nombre }
    return render(request, "proyecto/miembroEditar.html", context)




def eliminarProyecto(request,proyecto_id):
    """
       **Eliminar Proyecto:**
        03/09/2021
        Vista utilizada para elimiar un proyecto.
        Solicita el id del proyecto
    """
    print(proyecto_id)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    proyecto.delete()

    return redirect("/home/proyectos/")

def iniciarProyecto(request, proyecto_id):
    """
       **Iniciar Proyecto:**
        03/09/2021
        Vista utilizada para iniciar el proyecto .
        Solicita el id del proyecto
    """
    proyecto=Proyecto.objects.get(pk=proyecto_id)
    miembros=Miembro.objects.filter(proyectos=proyecto)
    proyecto.estado="ACTIVO"
    context = {"proyecto_id": proyecto_id,"proyecto": proyecto, "miembros": miembros}
    return render(request,"desarrollo/desarrollo.html", context)
