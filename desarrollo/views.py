# from audioop import reverse
from django.urls import reverse
from django.shortcuts import render, redirect

# Create your views here.
from desarrollo.forms import UserStoryForms, UserStoryMiembroForms, PlanningPokerForms
from desarrollo.models import UserStory, EstimacionPlanificada
from proyecto.models import Proyecto, Miembro


def desarrollo(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    proyecto_actual.iniciar_proyecto()
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual}
    return render(request, "desarrollo/desarrollo.html", context)


def productBacklog(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    userStory = UserStory.objects.filter(proyecto=proyecto_id, estado_desarrollo=UserStory.EN_PRODUCT_BACKLOG)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'userStory': userStory}
    return render(request, "desarrollo/productBacklog.html", context)


def crearUserStory(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

    form = UserStoryForms(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            nombre_user_story_form = data['nombre']
            nombre_user_story = UserStory.objects.filter(nombre=nombre_user_story_form)
            if not nombre_user_story.exists():
                form.instance.proyecto = proyecto_actual
                form.save()

                return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))
            else:
                error = True
                context = {"error": error, "proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form}
                return render(request, 'desarrollo/userStory/crear.html', context)

    else:
        form = UserStoryForms()

    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form}
    return render(request, "desarrollo/userStory/crear.html", context)


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


def eliminarUserStory(request, proyecto_id, user_story_id):
    user_story = UserStory.objects.get(pk=user_story_id)
    user_story.delete()
    return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))


def sprintPlanning(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    userStory = UserStory.objects.filter(estado_desarrollo=UserStory.EN_SPRINT_PLANNING, proyecto=proyecto_id)
    context = {"proyecto_id": proyecto_id, 'userStory': userStory, "proyecto": proyecto_actual}
    return render(request, "desarrollo/sprintPlanning.html", context)


def sprint_planning_estado(request, proyecto_id, user_story_id):
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    user_story_actual.estado_desarrollo = UserStory.EN_SPRINT_PLANNING
    user_story_actual.save()
    return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))


def product_backlog_estado(request, proyecto_id, user_story_id):
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    user_story_actual.estado_desarrollo = UserStory.EN_PRODUCT_BACKLOG
    user_story_actual.user=None
    user_story_actual.save()
    return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))


def asignarMiembroUS(request, proyecto_id, user_story_id):
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    if request.method == "POST":
        form = UserStoryMiembroForms(request.POST or None, instance=user_story_actual)
        if form.is_valid():
            form.instance.save()
            return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = UserStoryMiembroForms(instance=user_story_actual)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form, 'user_story': user_story_actual}
    return render(request, "desarrollo/asignarMiembroUS.html", context)


def planningPoker(request, proyecto_id, user_story_id):
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(proyectos=proyecto_actual, miembro=request.user)

    if request.user == user_story_actual.miembro_asignado or miembro.rol.nombre=='Scrum Master':
        estimacion, fue_creado= EstimacionPlanificada.objects.get_or_create(user_story=user_story_actual)

        if request.method == "POST":
            form = PlanningPokerForms(request.POST or None, instance=estimacion)

            if form.is_valid():
                estimacion= EstimacionPlanificada.objects.get(user_story=user_story_actual)
                data = form.cleaned_data
                estimacion_scrum=data["estimacion_scrum"]
                estimacion_miembro = data["estimacion_miembro"]
                if miembro.rol.nombre == 'Scrum Master':
                    estimacion.estimacion_scrum=estimacion_scrum
                else:
                    estimacion.estimacion_miembro=estimacion_miembro
                estimacion.save()
                if estimacion.estimacion_miembro > 0 and estimacion.estimacion_scrum > 0:
                    user_story_actual.estimacion= (estimacion.estimacion_miembro + estimacion.estimacion_scrum)/2
                    user_story_actual.save()
                return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))
        else:
            form = PlanningPokerForms(instance=estimacion)
            if miembro.rol.nombre=='Scrum Master':
                form.fields['estimacion_miembro'].disabled = True
            else:
                form.fields['estimacion_scrum'].disabled = True

    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form, 'user_story': user_story_actual}

    return render(request, "desarrollo/planningPoker.html", context)