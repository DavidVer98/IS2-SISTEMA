from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse
from guardian.shortcuts import assign_perm

from proyecto.models import Proyecto

# Create your views here.
from django.contrib.auth.models import Group, Permission

from user.models import User
from .models import Rol
from proyecto.forms import ProyectoForm, ProyectoCrearForms, setMiembroForms, CrearGrupo, EditarGrupo, \
    editar_rolmiembro_form, permissions
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

def setScrum(request, proyecto, user, rol):
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
    context = {}
    if request.method == "POST":
        form = ProyectoCrearForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nombre = data['nombre_proyecto']
            user = data['scrum_master']
            form.save()
            proyecto=Proyecto.objects.get(nombre_proyecto=nombre)
            rol= scrumRol(proyecto.pk)
            setScrum(request, proyecto, user, rol)
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
        form.fields["rol"].queryset = Proyecto.objects.get(pk=proyecto_id).roles
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
    rol= Rol.objects.get(id=rol_id)
    if not(Miembro.objects.filter(rol=rol).exists()): # validar eliminacion de rol
        grupo= rol.group
        grupo.delete()
        rol.delete()
        return listarRol(request, proyecto_id)
    else:
        return redirect(reverse("listaRol",kwargs={"proyecto_id":proyecto_id}))

def eliminarmiembro(request, proyecto_id, miembro_id):
    miembro = Miembro.objects.get(pk=miembro_id)
    usuario = miembro.miembro
    usuario.groups.remove(miembro.rol.group)
    miembro.delete()
    return getMiembros(request, proyecto_id)

def editar_rolmiembro(request, proyecto_id, miembro_id):

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
    else:
        form=editar_rolmiembro_form(instance=miembro)
        form.fields["rol"].queryset = Proyecto.objects.get(pk=proyecto_id).roles

    context = {"proyecto_id": proyecto_id, "miembro_id": miembro_id, "form": form}
    return render(request, "proyecto/miembroEditar.html", context)




def eliminarProyecto(request,proyecto_id):
    print(proyecto_id)
    proyecto=Proyecto.objects.get(id=proyecto_id)
    proyecto.delete()

    return redirect("/home/proyectos/")
