# from audioop import reverse
import json

from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Sum
# Create your views here.
from desarrollo.forms import UserStoryForms, UserStoryMiembroForms, PlanningPokerForms
from desarrollo.models import UserStory, EstimacionPlanificada
from proyecto.models import Proyecto, Miembro
from guardian.decorators import permission_required_or_403

from user.models import User


@permission_required_or_403('VER_PROYECTO', (Proyecto, 'id', 'proyecto_id'))
def desarrollo(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    proyecto_actual.iniciar_proyecto()
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual}
    return render(request, "desarrollo/desarrollo.html", context)


@permission_required_or_403('VER_PRODUCT_BACKLOG', (Proyecto, 'id', 'proyecto_id'))
def productBacklog(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    userStory = UserStory.objects.filter(proyecto=proyecto_id, estado_desarrollo=UserStory.EN_PRODUCT_BACKLOG)
    # userStory.order_by('-prioridad')
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'userStory': userStory}
    return render(request, "desarrollo/productBacklog.html", context)


@permission_required_or_403('CREAR_USER_STORY', (Proyecto, 'id', 'proyecto_id'))
def crearUserStory(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    error=False
    form = UserStoryForms(request.POST or None)
    if request.method == "POST":
        if form.is_valid():

            data = form.cleaned_data
            nombre_user_story_form = data['nombre']
            nombre_user_story = UserStory.objects.filter(nombre=nombre_user_story_form)
            if not nombre_user_story.exists():
                form.instance.proyecto = proyecto_actual
                form.save()
                user_story_creado = UserStory.objects.get(nombre=nombre_user_story_form)
                EstimacionPlanificada.objects.get_or_create(user_story=user_story_creado)
                return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))
            else:
                error = True

    form = UserStoryForms()
    form.fields['prioridad'].choices.remove((4,'Superalta'))
    form.fields['prioridad'].choices=form.fields['prioridad'].choices

    context = {"error": error, "proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form}
    return render(request, "desarrollo/userStory/crear.html", context)


@permission_required_or_403('EDITAR_USER_STORY', (Proyecto, 'id', 'proyecto_id'))
def editarUserStory(request, proyecto_id, user_story_id):
    user_story = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

    if request.method == "POST":
        form = UserStoryForms(request.POST or None, instance=user_story)

        if form.is_valid():
            user_story = UserStory.objects.get(pk=user_story_id)
            data = form.cleaned_data
            nombre_user_story_form = data['nombre']
            user_story_filtro = UserStory.objects.filter(nombre=nombre_user_story_form)
            if nombre_user_story_form == user_story.nombre or not user_story_filtro.exists():
                form.instance.proyecto = proyecto_actual
                form.instance.save()
                return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))
            else:
                error = True
                context = {"error": error, "proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form}
                return render(request, 'desarrollo/userStory/editar.html', context)
    else:
        form = UserStoryForms(instance=user_story)

    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form, 'user_story': user_story}
    return render(request, "desarrollo/userStory/editar.html", context)


@permission_required_or_403('ELIMINAR_USER_STORY', (Proyecto, 'id', 'proyecto_id'))
def eliminarUserStory(request, proyecto_id, user_story_id):
    user_story = UserStory.objects.get(pk=user_story_id)
    user_story.delete()
    return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))


@permission_required_or_403('VER_SPRINT_PLANNING', (Proyecto, 'id', 'proyecto_id'))
def sprintPlanning(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    user_stories = UserStory.objects.filter(estado_desarrollo=UserStory.EN_SPRINT_PLANNING, proyecto=proyecto_id)
    estimacion_total = user_stories.aggregate(Sum("estimacion")).get('estimacion__sum')

    miembros = Miembro.objects.filter(miembro_id__in=user_stories.values("miembro_asignado_id"),
                                      proyectos_id__exact=proyecto_id)
    capacidad_miembros = miembros.aggregate(Sum("produccion_por_semana")).get('produccion_por_semana__sum')
    if capacidad_miembros is None: capacidad_miembros = 0

    context = {"proyecto_id": proyecto_id, 'userStory': user_stories, "proyecto": proyecto_actual,
               "estimacion_total": estimacion_total, "capacidad_miembros": capacidad_miembros}
    return render(request, "desarrollo/sprintPlanning.html", context)


@permission_required_or_403('PLANIFICAR_SPRINT', (Proyecto, 'id', 'proyecto_id'))
def sprint_planning_estado(request, proyecto_id, user_story_id):
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    user_story_actual.estado_desarrollo = UserStory.EN_SPRINT_PLANNING
    user_story_actual.save()
    return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))


@permission_required_or_403('PLANIFICAR_SPRINT', (Proyecto, 'id', 'proyecto_id'))
def product_backlog_estado(request, proyecto_id, user_story_id):
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
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
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
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form, 'user_story': user_story_actual}
    return render(request, "desarrollo/asignarMiembroUS.html", context)


@permission_required_or_403('ESTIMAR_USER_STORY', (Proyecto, 'id', 'proyecto_id'))
def planningPoker(request, proyecto_id, user_story_id):
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    if request.user == user_story_actual.miembro_asignado or proyecto_actual.scrum_master == request.user:
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
                       'user_story': user_story_actual}
            return render(request, "desarrollo/planningPoker.html", context)

    return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))


def iniciarSprint(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    user_stories = UserStory.objects.filter(proyecto=proyecto_actual, estado_desarrollo=UserStory.EN_SPRINT_PLANNING)

    error = False
    if user_stories.exists():
        for user_story in user_stories:
            if user_story.estimacion == 0:
                error = True

        if not error:
            for user_story in user_stories:
                user_story.estado_desarrollo = UserStory.EN_SPRINT_BACKLOG
                user_story.save()
            return redirect(reverse('sprintBacklog', kwargs={'proyecto_id': proyecto_id}))
    return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))



def sprintBacklog(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    user_stories = UserStory.objects.filter(proyecto=proyecto_actual, estado_desarrollo=UserStory.EN_SPRINT_BACKLOG)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, "user_stories": user_stories}

    return render(request, "desarrollo/sprintBacklog.html", context)

def estadoUS(request, proyecto_id):
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        estadoUS = received_json_data['estado']
        userstory_pk = received_json_data['us_id']
        user_story = UserStory.objects.get(pk = userstory_pk)
        user_story.estado_sprint = estadoUS
        user_story.save()

    return render(request, 'home/index.html')