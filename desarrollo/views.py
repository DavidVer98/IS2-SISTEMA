# from audioop import reverse
from django.urls import reverse
from django.shortcuts import render, redirect

# Create your views here.
from desarrollo.forms import UserStoryForms
from desarrollo.models import UserStory
from proyecto.models import Proyecto


def desarrollo(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    proyecto_actual.iniciar_proyecto()
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual}
    return render(request, "desarrollo/desarrollo.html", context)


def productBacklog(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    userStory = UserStory.objects.filter(proyecto=proyecto_id)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'userStory': userStory}
    return render(request, "desarrollo/productBacklog.html", context)


def crearUserStory(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

    form = UserStoryForms(request.POST or None)
    if request.method == "POST":
        # data = form.cleaned_data
        if form.is_valid():
            form.instance.proyecto = proyecto_actual
            form.save()
            return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = UserStoryForms()

    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form}
    return render(request, "desarrollo/userStory/crear.html", context)


def editarUserStory(request, proyecto_id, user_story_id):
    user_story = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

    if request.method == "POST":
        form = UserStoryForms(request.POST or None, instance=user_story)
        # data = form.cleaned_data
        if form.is_valid():
            form.instance.proyecto = proyecto_actual
            form.instance.save()
            return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = UserStoryForms(instance=user_story)

    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form, 'user_story': user_story}
    return render(request, "desarrollo/userStory/editar.html", context)

def eliminarUserStory(request, proyecto_id, user_story_id):
    user_story = UserStory.objects.get(pk=user_story_id)
    user_story.delete()
    return redirect(reverse('productBacklog', kwargs={'proyecto_id': proyecto_id}))

# def sprintPlanning(request):
#     return render(request, )
