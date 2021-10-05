# from audioop import reverse
import json
from datetime import datetime

from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Sum
# Create your views here.
from desarrollo.forms import UserStoryForms, UserStoryMiembroForms, PlanningPokerForms, UserStoryRegistroForms
from desarrollo.models import UserStory, EstimacionPlanificada, RegistroUserStory
from desarrollo.forms import UserStoryForms, UserStoryMiembroForms, PlanningPokerForms
from desarrollo.models import UserStory, EstimacionPlanificada, Sprint
from proyecto.models import Proyecto, Miembro
from guardian.decorators import permission_required_or_403

from user.models import User


@permission_required_or_403('VER_PROYECTO', (Proyecto, 'id', 'proyecto_id'))
def desarrollo(request, proyecto_id):
    """
       Vista de Desarrollo:
        19/09/2021
        Vista en la cual se muestra el menu inicial del desarollo de
        un proyecto.
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    proyecto_actual.iniciar_proyecto()
    miembro = Miembro.objects.get(miembro = request.user, proyectos=proyecto_actual)
    print(miembro.rol)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'miembro':miembro}
    return render(request, "desarrollo/desarrollo.html", context)


@permission_required_or_403('VER_PRODUCT_BACKLOG', (Proyecto, 'id', 'proyecto_id'))
def productBacklog(request, proyecto_id):
    """
               Vista del Product Backlog:
                19/09/2021
                Vista en la cual se despliega la lista de user stories que
                se van a utilizar en un sprint
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    userStory = UserStory.objects.filter(proyecto=proyecto_id, estado_desarrollo=UserStory.EN_PRODUCT_BACKLOG)
    # userStory.order_by('-prioridad')
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'userStory': userStory, 'miembro':miembro}
    return render(request, "desarrollo/productBacklog.html", context)


@permission_required_or_403('CREAR_USER_STORY', (Proyecto, 'id', 'proyecto_id'))
def crearUserStory(request, proyecto_id):
    """
           Vista para crear User Stories:
            19/09/2021
            Vista en la cual se permite la creacion de user stories con
            ciertos parametros definidos.
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    error=False
    form = UserStoryForms(request.POST or None)
    if request.method == "POST":
        if form.is_valid():

            data = form.cleaned_data
            nombre_user_story_form = data['nombre']
            nombre_user_story = UserStory.objects.filter(nombre=nombre_user_story_form, proyecto=proyecto_actual)
            if not nombre_user_story.exists():
                form.instance.proyecto = proyecto_actual
                form.save()
                user_story_creado = UserStory.objects.get(nombre=nombre_user_story_form, proyecto=proyecto_actual)
                EstimacionPlanificada.objects.get_or_create(user_story=user_story_creado)
                return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))
            else:
                error = True

    form = UserStoryForms()
    form.fields['prioridad'].choices.remove((4, 'Super Alta'))
    form.fields['prioridad'].choices = form.fields['prioridad'].choices
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)

    context = {"error": error, "proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form,
               'miembro': miembro}
    return render(request, "desarrollo/userStory/crear.html", context)


@permission_required_or_403('EDITAR_USER_STORY', (Proyecto, 'id', 'proyecto_id'))
def editarUserStory(request, proyecto_id, user_story_id):
    """
           Vista para editar User Stories:
            19/09/2021
            Vista en la cual se permite la edicion de user stories con
            ciertos parametros definidos.
    """
    user_story = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    error = False
    if request.method == "POST":
        form = UserStoryForms(request.POST or None, instance=user_story)

        if form.is_valid():
            user_story = UserStory.objects.get(pk=user_story_id)
            data = form.cleaned_data
            nombre_user_story_form = data['nombre']
            user_story_filtro = UserStory.objects.filter(nombre=nombre_user_story_form, proyecto=proyecto_actual)
            if nombre_user_story_form == user_story.nombre or not user_story_filtro.exists():
                form.instance.proyecto = proyecto_actual
                form.instance.save()
                return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))
            else:
                error = True

    form = UserStoryForms(instance=user_story)
    form.fields['prioridad'].choices.remove((4, 'Super Alta'))
    form.fields['prioridad'].choices = form.fields['prioridad'].choices
    context = {"error": error, "proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form,
               'miembro': miembro, 'user_story': user_story}
    return render(request, "desarrollo/userStory/editar.html", context)


@permission_required_or_403('ELIMINAR_USER_STORY', (Proyecto, 'id', 'proyecto_id'))
def eliminarUserStory(request, proyecto_id, user_story_id):
    """
               Vista para eliminar User Stories:
                19/09/2021
                Vista en la cual se permite la eliminacion de user stories
    """
    user_story = UserStory.objects.get(pk=user_story_id)
    user_story.delete()
    return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))


@permission_required_or_403('VER_SPRINT_PLANNING', (Proyecto, 'id', 'proyecto_id'))
def sprintPlanning(request, proyecto_id):
    """
               Vista para la planeacion de un Sprint:
                19/09/2021
                Vista en la cual se lleva a cabo la planeacion de un sprint, asignando
                cada user story a un miembro y estimando la duracion de este.
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    user_stories = UserStory.objects.filter(estado_desarrollo=UserStory.EN_SPRINT_PLANNING, proyecto=proyecto_id)
    estimacion_total = user_stories.aggregate(Sum("estimacion")).get('estimacion__sum')
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)

    miembros = Miembro.objects.filter(miembro_id__in=user_stories.values("miembro_asignado_id"),
                                      proyectos_id__exact=proyecto_id)
    capacidad_miembros = miembros.aggregate(Sum("produccion_por_semana")).get('produccion_por_semana__sum')
    if not (capacidad_miembros is None or capacidad_miembros == 0):
        fecha_fin = estimacion_total / capacidad_miembros
        proyecto_actual.duracion_semanal_sprint_actual = fecha_fin
        proyecto_actual.save()
        dias = fecha_fin - int(fecha_fin)
        dias = round(dias * 5)
    else:
        fecha_fin = 0
        dias = 0
        capacidad_miembros = 0
    if estimacion_total is None: estimacion_total = 0
    context = {"proyecto_id": proyecto_id, 'userStory': user_stories, "proyecto": proyecto_actual,
               "estimacion_total": estimacion_total, "capacidad_miembros": capacidad_miembros, 'miembro': miembro,
               'fecha_fin': int(fecha_fin), 'dias': dias}
    return render(request, "desarrollo/sprintPlanning.html", context)


@permission_required_or_403('PLANIFICAR_SPRINT', (Proyecto, 'id', 'proyecto_id'))
def sprint_planning_estado(request, proyecto_id, user_story_id):
    """
              Metodo para gestion de user story:
               19/09/2021
               Metodo en el que se cambia el estado de un user story cuando
               pasa al sprint planning
    """
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    user_story_actual.estado_desarrollo = UserStory.EN_SPRINT_PLANNING
    user_story_actual.save()
    return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))


@permission_required_or_403('PLANIFICAR_SPRINT', (Proyecto, 'id', 'proyecto_id'))
def product_backlog_estado(request, proyecto_id, user_story_id):
    """
               Metodo para gestion de user story:
                19/09/2021
                Metodo en el que se reinicia las configuraciones de un user stories
                en caso de que se retire de un sprint
    """
    # se reinician los valores del user story al pasarlo al product backlog
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    user_story_actual.estado_desarrollo = UserStory.EN_PRODUCT_BACKLOG
    user_story_actual.miembro_asignado = None
    user_story_actual.estimacion = 0

    estimaciones = EstimacionPlanificada.objects.get(user_story=user_story_actual)
    estimaciones.estimacion_miembro = 0
    estimaciones.estimacion_scrum = 0
    estimaciones.save()
    user_story_actual.save()
    return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))


@permission_required_or_403('PLANIFICAR_SPRINT', (Proyecto, 'id', 'proyecto_id'))
def asignarMiembroUS(request, proyecto_id, user_story_id):
    """
           Metodo para asignar un user story:
            19/09/2021
            Metodo en el que se asigna un user story a un miembro
            dentro del proyecto
    """
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    if request.method == "POST":
        form = UserStoryMiembroForms(request.POST or None, instance=user_story_actual)
        if form.is_valid():
            form.instance.save()
            estimacion_anterior = EstimacionPlanificada.objects.get(user_story=user_story_actual)
            estimacion_anterior.estimacion_miembro = 0
            user_story_actual.estimacion = 0
            user_story_actual.save()
            estimacion_anterior.save()
            return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = UserStoryMiembroForms(instance=user_story_actual)
        form.fields['miembro_asignado'].queryset = User.objects.filter(miembro__proyectos=proyecto_actual).exclude(
            pk=proyecto_actual.scrum_master.pk)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form, 'user_story': user_story_actual,
               'miembro': miembro}
    return render(request, "desarrollo/asignarMiembroUS.html", context)


@permission_required_or_403('ESTIMAR_USER_STORY', (Proyecto, 'id', 'proyecto_id'))
def planningPoker(request, proyecto_id, user_story_id):
    """
           Vista de planning poker:
            19/09/2021
            Vista en la cual se lleva a cabo el planning poker, primeramente el
            scrum master realiza su estimacion en el sprint planning y luego el miembro asignado
            realiza su estimacion.
    """
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)

    if (request.user == user_story_actual.miembro_asignado or proyecto_actual.scrum_master == request.user) and \
            user_story_actual.estado_desarrollo == UserStory.EN_SPRINT_PLANNING:
        estimacion = EstimacionPlanificada.objects.get(user_story=user_story_actual)

        if request.method == "POST":
            form = PlanningPokerForms(request.POST or None, instance=estimacion)

            if form.is_valid():
                estimacion = EstimacionPlanificada.objects.get(user_story=user_story_actual)
                data = form.cleaned_data
                estimacion_scrum = data["estimacion_scrum"]
                estimacion_miembro = data["estimacion_miembro"]

                # se guardan los datos cambiados dependiendo del usuario del request
                if proyecto_actual.scrum_master == request.user:
                    estimacion.estimacion_scrum = estimacion_scrum
                else:
                    estimacion.estimacion_miembro = estimacion_miembro
                estimacion.save()

                # se actualiza la estimacion final de user story
                if estimacion.estimacion_miembro > 0 and estimacion.estimacion_scrum > 0:
                    user_story_actual.estimacion = (estimacion.estimacion_miembro + estimacion.estimacion_scrum) / 2
                else:
                    user_story_actual.estimacion = 0
                user_story_actual.save()
                return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))
        else:
            form = PlanningPokerForms(instance=estimacion)
            # se deshabilita el field correspondiente en el form
            if proyecto_actual.scrum_master == request.user:
                form.fields['estimacion_miembro'].disabled = True
            else:
                form.fields['estimacion_scrum'].disabled = True

            context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form,
                       'user_story': user_story_actual, 'miembro': miembro}

            return render(request, "desarrollo/planningPoker.html", context)

    return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))


def iniciarSprint(request, proyecto_id):
    """
           Vista para iniciar sprint:
            19/09/2021
            Vista en la cual se mueven los user stories al sprint backlog, cambiando
            el estado de cada uno a 'EN SPRINT BACKLOG'
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    user_stories = UserStory.objects.filter(proyecto=proyecto_actual, estado_desarrollo=UserStory.EN_SPRINT_PLANNING)
    sprint_activo = UserStory.objects.filter(proyecto=proyecto_actual, estado_desarrollo=UserStory.EN_SPRINT_BACKLOG)
    error = False
    if user_stories.exists() and not sprint_activo.exists():
        for user_story in user_stories:
            if user_story.estimacion == 0:
                error = True

        if not error:
            sprint = Sprint.objects.create(nombre=str(datetime.now), proyecto=proyecto_actual)
            for user_story in user_stories:
                sprint.user_stories.add(user_story)
                user_story.estado_desarrollo = UserStory.EN_SPRINT_BACKLOG
                user_story.save()


            return redirect(reverse('sprintBacklog', kwargs={'proyecto_id': proyecto_id}))
    return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))


def terminarSprint(request, proyecto_id):

    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    sprint_actual = Sprint.objects.get(proyecto=proyecto_actual, estado=Sprint.ACTIVO)
    sprint_actual.estado = Sprint.FINALIZADO
    sprint_actual.fecha_fin = datetime.now()
    proyecto_actual.duracion_semanal_sprint_actual = 0

    for user_story in sprint_actual.user_stories.all():

        if user_story.estado_sprint != UserStory.RELASE:
            user_story.estado_desarrollo=UserStory.EN_PRODUCT_BACKLOG
            user_story.prioridad=UserStory.SUPERALTA
            user_story.estado_sprint=UserStory.TO_DO
            user_story.estimacion = 0
            user_story.miembro_asignado = None
            user_story.save()

            estimacion = EstimacionPlanificada.objects.get(user_story=user_story)
            estimacion.estimacion_miembro = 0
            estimacion.estimacion_scrum = 0
            estimacion.save()

    proyecto_actual.save()
    sprint_actual.save()
    return redirect(reverse('sprintBacklog', kwargs={'proyecto_id': proyecto_id}))


def sprintBacklog(request, proyecto_id):
    """
           Vista de sprint backlog:
            19/09/2021
            Vista en la cual se listan los user stories que pertenencen al sprint activo.
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    estimacion_total = proyecto_actual.duracion_semanal_sprint_actual
    dias = estimacion_total - int(estimacion_total)
    dias = round(dias * 5)

    user_stories = UserStory.objects.filter(proyecto=proyecto_actual, estado_desarrollo=UserStory.EN_SPRINT_BACKLOG)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, "user_stories": user_stories,
               'miembro': miembro, 'estimacion_total': int(estimacion_total), 'dias': dias}

    return render(request, "desarrollo/sprintBacklog.html", context)


def estadoUS(request, proyecto_id):
    """
           Metodo para la gestion de un user story:
            19/09/2021
            Metodo en el cual se permite el cambio de estado de un user story
    """
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        estadoUS = received_json_data['estado']
        userstory_pk = received_json_data['us_id']
        user_story = UserStory.objects.get(pk=userstory_pk)
        user_story.estado_sprint = estadoUS
        user_story.save()

    return render(request, 'home/index.html')

def registrarUS(request, proyecto_id, user_story_id):
    user_story = UserStory.objects.get(pk = user_story_id)
    registro = RegistroUserStory.objects.filter(user_story = user_story)
    horas_totales = registro.aggregate(Sum("horas_trabajadas")).get('horas_trabajadas__sum')
    contador_registro = None
    if RegistroUserStory.objects.filter(user_story = user_story).exists():
        print(contador_registro)
        contador_registro = registro.all().last().contador_registro


    if request.method == "POST":
        form = UserStoryRegistroForms(request.POST or None)
        if form.is_valid():
            form.instance.user_story = user_story
            if horas_totales and contador_registro:
                form.instance.horas_totales = form.instance.horas_trabajadas + horas_totales
                form.instance.contador_registro = contador_registro + 1
            else:
                form.instance.horas_totales = form.instance.horas_trabajadas
                form.instance.contador_registro = 1
            form.save()
            return redirect(reverse('sprintBacklog', kwargs={'proyecto_id': proyecto_id}))
            print("horas totales",form.instance.horas_totales)
    else:
        print("numero de registro",contador_registro)
        if(contador_registro):
            registro1 = RegistroUserStory.objects.get(user_story=user_story , contador_registro = contador_registro)
            form = UserStoryRegistroForms(instance=registro1)
        else:
            form = UserStoryRegistroForms()


    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro = request.user, proyectos=proyecto_actual)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'miembro':miembro,"form":form,"user_story":user_story}


    return render(request, "desarrollo/userStory/registro.html", context)

def registroUSActual(request, proyecto_id, user_story_id):
    user_story = UserStory.objects.get(pk = user_story_id)
    registro = RegistroUserStory.objects.filter(user_story = user_story)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    context = {"proyecto_id": proyecto_id, 'user_story':user_story,"proyecto": proyecto_actual ,'registro':registro, 'miembro':miembro}

    return render(request, "desarrollo/userStory/registroUSActual.html", context)