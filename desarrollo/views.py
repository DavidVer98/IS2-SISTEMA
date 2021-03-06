# from audioop import reverse
import json
from copy import deepcopy
from datetime import datetime

from datetime import datetime, timedelta
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

from django.http import JsonResponse, HttpResponse

from user.models import User
from user.views import msg3, msg4
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa




@permission_required_or_403('VER_PROYECTO', (Proyecto, 'id', 'proyecto_id'))
def desarrollo(request, proyecto_id):
    """
       Vista de Desarrollo:
        19/09/2021
        Vista en la cual se muestra el menu inicial del desarollo de
        un proyecto.
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    print(miembro.rol)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'miembro': miembro}
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
    userStoryActivos = UserStory.objects.filter(proyecto=proyecto_id, estado_desarrollo=UserStory.EN_SPRINT_BACKLOG)
    userStoryEliminados = UserStory.objects.filter(proyecto=proyecto_id,estado_desarrollo=UserStory.ELIMINADO)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)

    userStor_general = userStory | userStoryActivos | userStoryEliminados
    userStor_general.order_by('-prioridad')

    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'userStory': userStor_general, 'miembro': miembro}
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
    error = False
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
    registros = RegistroUserStory.objects.filter(user_story__pk =  user_story_id)
    user_story = UserStory.objects.get(pk=user_story_id)
    if registros.exists():
        user_story.estado_desarrollo = UserStory.ELIMINADO
        user_story.save()
    else:
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
    import math
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    user_stories = UserStory.objects.filter(estado_desarrollo=UserStory.EN_SPRINT_PLANNING, proyecto=proyecto_id)
    estimacion_total = user_stories.aggregate(Sum("estimacion")).get('estimacion__sum')
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)

    miembros = Miembro.objects.filter(miembro_id__in=user_stories.values("miembro_asignado_id"),
                                      proyectos_id__exact=proyecto_id)
    capacidad_miembros = miembros.aggregate(Sum("produccion_diaria")).get(
        'produccion_diaria__sum')
    if not (capacidad_miembros is None or capacidad_miembros == 0):
        capacidad_miembros *= proyecto_actual.duracion_dias_sprint
        fecha_fin = estimacion_total / capacidad_miembros * proyecto_actual.duracion_dias_sprint
        proyecto_actual.duracion_dias_sprint_actual = fecha_fin
        proyecto_actual.save()
        dias = math.ceil(fecha_fin)
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
            "mensaje aca sipa"
            return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = UserStoryMiembroForms(instance=user_story_actual)
        form.fields['miembro_asignado'].queryset = User.objects.filter(miembro__proyectos=proyecto_actual).exclude(
            pk=proyecto_actual.scrum_master.pk)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form, 'user_story': user_story_actual,
               'miembro': miembro}
    return render(request, "desarrollo/asignarMiembroUS.html", context)


@permission_required_or_403('REASIGNAR_MIEMBRO', (Proyecto, 'id', 'proyecto_id'))
def reasignarMiembroUS(request, proyecto_id, user_story_id):
    """
              **reasignarMiembroUS:**
              11/10/2021
              Metodo en el que se reasigna un miembro a un user story
            dentro del sprint

    """
    user_story_actual = UserStory.objects.get(pk=user_story_id)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    if request.method == "POST":
        form = UserStoryMiembroForms(request.POST or None, instance=user_story_actual)
        if form.is_valid():
            form.instance.save()
            return redirect(reverse('sprintBacklog', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = UserStoryMiembroForms(instance=user_story_actual)
        form.fields['miembro_asignado'].queryset = User.objects.filter(miembro__proyectos=proyecto_actual).exclude(
            pk=proyecto_actual.scrum_master.pk)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'form': form, 'user_story': user_story_actual,
               'miembro': miembro}
    return render(request, "desarrollo/reasignarMiembroUS.html", context)


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


@permission_required_or_403('INICIAR_SPRINT', (Proyecto, 'id', 'proyecto_id'))
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
    print(sprint_activo.values())
    if user_stories.exists() and not sprint_activo.exists():
        for user_story in user_stories:
            if user_story.estimacion == 0:
                error = True

        if not error:
            fecha = proyecto_actual.nombre_proyecto + " Sprint " + datetime.today().strftime('%Y-%m-%d')
            sprint = Sprint.objects.create(nombre=fecha, proyecto=proyecto_actual)
            sprint.estimacion_total_us = user_stories.aggregate(Sum("estimacion")).get('estimacion__sum')
            sprint.duracion_estimada_sprint = proyecto_actual.duracion_dias_sprint_actual

            for user_story in user_stories:
                sprint.user_stories.add(user_story)
                user_story.estado_desarrollo = UserStory.EN_SPRINT_BACKLOG
                user_story.save()
            msg3(user_stories,proyecto_actual.nombre_proyecto,proyecto_actual.scrum_master.email)
            sprint.save()
            print("fecha", sprint.fecha_inicio)
            return redirect(reverse('sprintBacklog', kwargs={'proyecto_id': proyecto_id}))
    return redirect(reverse('sprintPlanning', kwargs={'proyecto_id': proyecto_id}))


@permission_required_or_403('TERMINAR_SPRINT', (Proyecto, 'id', 'proyecto_id'))
def terminarSprint(request, proyecto_id):
    """
                Metodo para la gestion de un sprint
                  11/10/2021
                  Metodo en el que se da por finalizado un sprint

    """

    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    try:
        sprint_actual = Sprint.objects.get(proyecto=proyecto_actual, estado=Sprint.ACTIVO)
    except Sprint.DoesNotExist:
        sprint_actual = None

    if sprint_actual is not None:

        sprint_actual.estado = Sprint.FINALIZADO
        sprint_actual.fecha_fin = datetime.now()
        proyecto_actual.duracion_dias_sprint_actual = 0
        lista = []
        for us in sprint_actual.user_stories.all():

            us.save()

            us.pk = None
            us.estado_desarrollo = UserStory.EN_REGISTRO_SPRINT
            us.save()

            lista.append(us)
            print("wat ", lista)

        sprint_actual.copia_user_stories.set(lista)

        for user_story in sprint_actual.user_stories.all():
            if user_story.estado_sprint != UserStory.RELEASE:
                user_story.estado_desarrollo = UserStory.EN_PRODUCT_BACKLOG
                user_story.prioridad = UserStory.SUPERALTA
                user_story.estado_sprint = UserStory.TO_DO
                user_story.estimacion = 0
                user_story.miembro_asignado = None
                user_story.save()

                estimacion = EstimacionPlanificada.objects.get(user_story=user_story)
                estimacion.estimacion_miembro = 0
                estimacion.estimacion_scrum = 0
                estimacion.save()
            else:
                #***
                user_story.estado_desarrollo = UserStory.EN_PRODUCT_BACKLOG
                user_story.save()

        proyecto_actual.save()
        sprint_actual.save()
        print("fecha fin", sprint_actual.fecha_fin)
    return redirect(reverse('sprintBacklog', kwargs={'proyecto_id': proyecto_id}))


@permission_required_or_403('VER_SPRINT_BACKLOG', (Proyecto, 'id', 'proyecto_id'))
def sprintBacklog(request, proyecto_id):
    """
           Vista de sprint backlog:
            19/09/2021
            Vista en la cual se listan los user stories que pertenencen al sprint activo.
    """
    import math
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    estimacion_total = proyecto_actual.duracion_dias_sprint_actual
    try:
        sprint_actual = Sprint.objects.get(estado=Sprint.ACTIVO, proyecto=proyecto_actual)
        dias = math.ceil(sprint_actual.duracion_estimada_sprint)
    except Sprint.DoesNotExist:
        dias = 0

    user_stories = UserStory.objects.filter(proyecto=proyecto_actual, estado_desarrollo=UserStory.EN_SPRINT_BACKLOG)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, "user_stories": user_stories,
               'miembro': miembro, 'estimacion_total': int(estimacion_total), 'dias': dias}

    return render(request, "desarrollo/sprintBacklog.html", context)


@permission_required_or_403('CAMBIO_ESTADO_US', (Proyecto, 'id', 'proyecto_id'))
def estadoUS(request, proyecto_id):
    """
           Metodo para la gestion de un user story:
            19/09/2021
            Metodo en el cual se permite el cambio de estado de un user story en la tabla kanban
    """
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        estadoUS = received_json_data['estado']
        userstory_pk = received_json_data['us_id']
        user_story = UserStory.objects.get(pk=userstory_pk)

        sprint = Sprint.objects.get(estado=Sprint.ACTIVO)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        registro = RegistroUserStory.objects.filter(user_story=user_story, sprint=sprint, usuario=proyecto.scrum_master.email) #registroScrum
        registroUser = RegistroUserStory.objects.filter(user_story=user_story, sprint=sprint,
                                                    usuario=request.user.email)  # registroUser
        ultimoreg = registro.all().last()
        # print(registro.exists(), "eee")
        print(registroUser.exists(), "eee")

        if estadoUS == "RELEASE" and user_story.estado_sprint =="QA" and registro.exists(): #[A] QA a RELEASE
            # print(registro, "eee")
            if ultimoreg.usuario==proyecto.scrum_master.email:
                msg4(user_story.miembro_asignado.email, user_story.miembro_asignado.username, ultimoreg.detalles,user_story.nombre, proyecto.nombre_proyecto,True)
                user_story.estado_sprint = estadoUS
                user_story.save()
                return render(request, 'home/index.html')

        elif estadoUS != "QA" and (estadoUS == "DOING" or estadoUS == "TO DO") and user_story.estado_sprint =="QA" and registro.exists():    #[R] QA a TO DO, DOING
            # print("entro?")
            if ultimoreg.usuario==proyecto.scrum_master.email:
                msg4(user_story.miembro_asignado.email, user_story.miembro_asignado.username, ultimoreg.detalles,user_story.nombre, proyecto.nombre_proyecto,False)
                user_story.estado_sprint = estadoUS
                user_story.save()
                return render(request, 'home/index.html')
        elif user_story.estado_sprint =="QA" and estadoUS == "DONE" : #[E] QA a DONE
            response = HttpResponse('Erro_400_bat')
            response.status_code = 400  # sample status code
            return response
        elif user_story.estado_sprint =="QA" and  (estadoUS == "DOING" or estadoUS == "TO DO") and not(registro.exists()) :#[E-R] QA a DOING, TO DO
            # print("AAA???")
            response = HttpResponse('Erro_400_bat')
            response.status_code = 400  # sample status code
            return response
        elif estadoUS == "RELEASE" and not (registro.exists()): #[E-A] QA a RELEASE
            response = HttpResponse('Erro_400_bat')
            response.status_code = 400  # sample status code
            return response
        elif estadoUS == "DONE" and  user_story.estado_sprint =="TO DO": #[E] TO DO a DONE
            response = HttpResponse('Erro_400_bat')
            response.status_code = 400  # sample status code
            return response
        elif estadoUS == "TO DO" and  user_story.estado_sprint =="DOING" and registroUser.exists(): #[E] DOING a TO DO
            response = HttpResponse('Erro_400_bat')
            response.status_code = 408  # sample status code
            return response
        elif estadoUS == "DONE" and  user_story.estado_sprint =="DOING" and not (registroUser.exists()): #[E] DOING a DONE
            response = HttpResponse('Erro_400_bat')
            response.status_code = 400  # sample status code
            return response
        elif estadoUS == "RELEASE" and  user_story.estado_sprint =="DONE" : #[E] DONE a RELEASE
            response = HttpResponse('Erro_400_bat')
            response.status_code = 408  # sample status code
            return response
    user_story.estado_sprint = estadoUS
    user_story.save()

    return render(request, 'home/index.html')


@permission_required_or_403('CREAR_REGISTRO_US', (Proyecto, 'id', 'proyecto_id'))
def registrarUS(request, proyecto_id, user_story_id):
    """
              Metodo para la gestion de un user story:
               11/10/2021
               Metodo que se utiliza para el registro de user storys nuevos o desechados de anteriores
               sprints
       """
    user_story = UserStory.objects.get(pk=user_story_id)
    sprint_actual = Sprint.objects.get(estado=Sprint.ACTIVO)
    registro = RegistroUserStory.objects.filter(user_story=user_story, sprint= sprint_actual)
    horas_totales = registro.aggregate(Sum("horas_trabajadas")).get('horas_trabajadas__sum')
    contador_registro = None
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)


    if RegistroUserStory.objects.filter(user_story=user_story,sprint = sprint_actual).exists():
        contador_registro = registro.all().last().contador_registro

    if request.method == "POST":
        form = UserStoryRegistroForms(request.POST or None)
        if form.is_valid():
            proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
            sprint = Sprint.objects.get(estado=Sprint.ACTIVO, proyecto=proyecto_actual)
            form.instance.user_story = user_story
            form.instance.nombre_user_story = user_story.nombre
            form.instance.sprint = sprint
            if horas_totales and contador_registro:
                form.instance.horas_totales = form.instance.horas_trabajadas + horas_totales
                form.instance.contador_registro = contador_registro + 1
                form.instance.usuario = user_story.miembro_asignado.email
            else:
                form.instance.horas_totales = form.instance.horas_trabajadas
                form.instance.contador_registro = 1
                form.instance.usuario = user_story.miembro_asignado.email
            if request.user == proyecto_actual.scrum_master:
                form.instance.usuario = proyecto_actual.scrum_master.email
                form.save()
            if (form.instance.usuario == request.user.email):
                form.save()
            return redirect(reverse('sprintBacklog', kwargs={'proyecto_id': proyecto_id}))
    else:
        form = UserStoryRegistroForms()
        if request.user == proyecto_actual.scrum_master:
            form.fields['horas_trabajadas'].disabled = True

    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'miembro': miembro, "form": form,
               "user_story": user_story, "contador_registro": contador_registro, "horas_totales": horas_totales}
    return render(request, "desarrollo/userStory/registro.html", context)


@permission_required_or_403('VER_REGISTRO_US', (Proyecto, 'id', 'proyecto_id'))
def registroUSActual(request, proyecto_id, user_story_id):
    """
                  Metodo para la gestion de un user story:
                  11/10/2021
                  Metodo en el que se utiliza para obtener el registro actual de actividades de un
                  User Story dentro de un sprint

    """
    sprint_actual = Sprint.objects.get(estado=Sprint.ACTIVO)
    user_story = UserStory.objects.get(pk=user_story_id)
    registro = RegistroUserStory.objects.filter(user_story=user_story,  sprint = sprint_actual)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    context = {"proyecto_id": proyecto_id, 'user_story': user_story, "proyecto": proyecto_actual, 'registro': registro,
               'miembro': miembro}

    return render(request, "desarrollo/userStory/registroUSActual.html", context)


@permission_required_or_403('VER_REGISTROS', (Proyecto, 'id', 'proyecto_id'))
def registroSprints(request, proyecto_id):
    """
                      Metodo para la gestion de sprints:
                      11/10/2021
                      Metodo que se utiliza para listar los sprints, tanto activos como culminados

    """

    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    sprints = Sprint.objects.filter(proyecto=proyecto_actual)

    nombre = 'Sprint ' + datetime.today().strftime('%Y-%m-%d')
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, "miembro": miembro, "sprints": sprints}
    return render(request, "desarrollo/registroSprints.html", context)


@permission_required_or_403('VER_REGISTROS', (Proyecto, 'id', 'proyecto_id'))
def registroUserStories(request, proyecto_id, sprint_id):
    """
                          Metodo para la gestion de user stories:
                          11/10/2021
                          Metodo que se ultiliza para visualizar la carga horaria y la descripcion de un User Story
                          en desarrrollo

    """

    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    registros = RegistroUserStory.objects.filter(sprint__id__exact=sprint_id)
    sprint_id = Sprint.objects.get(pk = sprint_id)
    suma_hora_registros = 0
    for registro in registros:
        suma_hora_registros += registro.horas_trabajadas
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, "miembro": miembro, "registros": registros,
               "suma_hora_registros": suma_hora_registros, 'sprint_id':sprint_id.pk}
    return render(request, "desarrollo/registroUserStories.html", context)


def burndown_chart(request, proyecto_id, sprint_id):
    """
            Metodo para la gestion de user stories:
              29/10/2021
            Metodo que se encarga de realizar la grafica
            burdown chart de todos los sprints
    """
    sprint_actual = Sprint.objects.get(id=sprint_id)
    for i in sprint_actual.copia_user_stories.all():
        print(i.miembro_asignado)
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)

    registros = RegistroUserStory.objects.filter(sprint=sprint_actual).values('fecha').order_by('fecha').annotate(
        sum=Sum('horas_trabajadas'))

    fecha_inicio = sprint_actual.fecha_inicio
    fecha_actual=datetime.now().date()

    if sprint_actual.fecha_fin is None:
        fecha_fin = fecha_actual
    else:
        fecha_fin = sprint_actual.fecha_fin

    cantidad = abs(fecha_fin - fecha_inicio).days + 1

    date_list = [fecha_fin - timedelta(days=x) for x in range(cantidad)]
    diccionario = {}

    for i in date_list:
        diccionario[i] = 0

    for date in date_list:
        for registro in registros.all():
            if registro["fecha"] == date:
                diccionario[date] += registro["sum"]

    array_horas_trabajadas = list(diccionario.values())
    array_horas_trabajadas.reverse()
    array_horas_trabajadas[0] = sprint_actual.estimacion_total_us - array_horas_trabajadas[0]

    for i, index in enumerate(array_horas_trabajadas, start=1):
        if i < len(array_horas_trabajadas):
            array_horas_trabajadas[i] = array_horas_trabajadas[i - 1] - array_horas_trabajadas[i]

    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'miembro': miembro, "sprint": sprint_actual,
               'array_horas_trabajadas': array_horas_trabajadas, 'fecha_actual': fecha_actual}
    return render(request, "desarrollo/graficos/burndown_chart.html", context)


def chart_sprint_activo(request, proyecto_id):
    """
            Metodo para la gestion de user stories:
              29/10/2021
            Metodo realiza el burdown chart en base a los registros sobre un sprint
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)


    if Sprint.objects.filter(proyecto=proyecto_actual,estado="Activo").exists():
        sprint = Sprint.objects.get(proyecto=proyecto_actual,estado="Activo")
        sprint_id = sprint.pk

        sprint_actual = Sprint.objects.get(id=sprint_id)
        proyecto_actual = Proyecto.objects.get(pk=proyecto_id)


        registros = RegistroUserStory.objects.filter(sprint=sprint_actual).values('fecha').order_by('fecha').annotate(
            sum=Sum('horas_trabajadas'))
        registros_user = RegistroUserStory.objects.filter(usuario=request.user.email, sprint=sprint_actual).values(
            'fecha').order_by('fecha').annotate(sum=Sum('horas_trabajadas'))

        fecha_inicio = sprint_actual.fecha_inicio
        fecha_actual = datetime.now().date()
        cantidad = abs(fecha_actual - fecha_inicio).days + 1
        base = datetime.now().date()
        date_list = [base - timedelta(days=x) for x in range(cantidad)]
        diccionario = {}
        diccionario_user_registro = {}

        for i in date_list:
            diccionario[i] = 0
            diccionario_user_registro[i] = 0

        for date in date_list:
            for registro in registros_user.all():
                if registro["fecha"] == date:
                    diccionario_user_registro[date] += registro["sum"]

        for date in date_list:
            for registro in registros.all():
                if registro["fecha"] == date:
                    diccionario[date] += registro["sum"]

        array_horas_trabajadas_user = list(diccionario_user_registro.values())
        array_horas_trabajadas = list(diccionario.values())
        array_horas_trabajadas_user.reverse()
        array_horas_trabajadas.reverse()
        array_horas_trabajadas_user[0] = sprint_actual.estimacion_total_us - array_horas_trabajadas_user[0]
        array_horas_trabajadas[0] = sprint_actual.estimacion_total_us - array_horas_trabajadas[0]

        for i, index in enumerate(array_horas_trabajadas, start=1):
            if i < len(array_horas_trabajadas):
                array_horas_trabajadas[i] = array_horas_trabajadas[i - 1] - array_horas_trabajadas[i]
                array_horas_trabajadas_user[i] = array_horas_trabajadas_user[i - 1] - array_horas_trabajadas_user[i]

        context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'miembro': miembro, "sprint": sprint_actual,
                   'array_horas_trabajadas': array_horas_trabajadas, 'fecha_actual': fecha_actual,
                   'array_horas_trabajadas_user': array_horas_trabajadas_user, 'cantidad': cantidad}
    else:
        context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'miembro': miembro}
    return render(request, "desarrollo/graficos/sprint_activo.html", context)

def historial_sprint(request, proyecto_id, sprint_id):
    """
            Metodo para la gestion de user stories:
              29/10/2021
            Metodo para visualizar todos los cambios hechos sobre un sprint
    """
    proyecto_actual = Proyecto.objects.get(pk = proyecto_id)
    sprint_actual = Sprint.objects.get(pk = sprint_id, proyecto =proyecto_actual )
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    print(miembro.rol)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, 'miembro': miembro, 'sprint_actual': sprint_actual}
    return render(request, "desarrollo/hisorial/hisorial_sprint.html", context)

def historial_sprint_backlog(request, proyecto_id, sprint_id):
    """
            Vista de sprint backlog:
            29/10/2021
            Vista en la cual se listan los user stories que pertenencen al sprint activo.
    """
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    estimacion_total = proyecto_actual.duracion_dias_sprint_actual
    dias = estimacion_total - int(estimacion_total)
    dias = round(dias * 5)
    sprint_actual = Sprint.objects.get(pk = sprint_id, proyecto = proyecto_actual)


    user_stories = sprint_actual.copia_user_stories
    print(user_stories.all())
    miembro = Miembro.objects.get(miembro=request.user, proyectos=proyecto_actual)
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual, "user_stories": user_stories.all(),
               'miembro': miembro, 'estimacion_total': int(estimacion_total), 'dias': dias, 'sprint_actual': sprint_actual}

    return render(request, "desarrollo/hisorial/historial_sprint_backlog.html", context)




def reporte_product_backlog(request, proyecto_id):
    """
            Reporte del product backlog:
                19/11/2021
            Genera un reporte pdf de un proyecto listando el estado de los user stories del mismo.
    """
    fecha=datetime.now()
    path = "desarrollo/reporte_product_backlog.html"
    proyecto_nombre = Proyecto.objects.get(pk=proyecto_id)
    user_stories = UserStory.objects.filter(proyecto_id=proyecto_id).exclude(estado_desarrollo='EN REGISTRO SPRINT')
    context = {"proyecto_id": proyecto_id,"user_stories":user_stories, "proyecto_nombre":proyecto_nombre,"fecha":fecha}

    html = render_to_string(path, context, request)
    io_bytes = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)

    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)


def reporte_sprint_backlog(request, proyecto_id):
    """
              Reporte del sprint backlog:
                  19/11/2021
              Genera un reporte pdf del sprint activo de un proyecto, citando los user stories con las horas trabajadas
              y planificadas de cada uno.
      """
    reporte = []
    fecha = datetime.now()
    path = "desarrollo/reporte_sprint_backlog.html"
    proyecto_actual= Proyecto.objects.get(pk=proyecto_id)
    user_stories = UserStory.objects.filter(proyecto_id=proyecto_id, estado_desarrollo='EN SPRINT BACKLOG').exclude(estado_desarrollo='EN REGISTRO SPRINT')

    try:
        sprint_actual = Sprint.objects.get(proyecto=proyecto_actual, estado='Activo')
        for user_story in user_stories.all():
            registros = RegistroUserStory.objects.filter(user_story=user_story, sprint=sprint_actual)
            suma = 0
            for registro in registros.all():
                suma += registro.horas_trabajadas

            reporte.append((user_story.nombre, suma, user_story.miembro_asignado.username,))

    except Sprint.DoesNotExist:
        pass

    context = {"proyecto_id": proyecto_id, "reportes":reporte, "proyecto_nombre": proyecto_actual,"fecha":fecha}

    html = render_to_string(path, context, request)
    io_bytes = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)

    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)


def reporte_sprint(request, proyecto_id, sprint_id):
    """
                 Reporte de sprints:
                     19/11/2021
                 Genera un reporte pdf del sprint seleccionado en un proyecto, donde se visualiza las horas trabajadas
                 y el usuario asignado.

         """
    fecha = datetime.now()
    path = "desarrollo/reporte_sprint.html"
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    sprint = Sprint.objects.get(pk=sprint_id, proyecto=proyecto_actual)
    user_stories = sprint.user_stories
    reporte_total=[]
    user_stories.order_by('-prioridad')
    for user_story in user_stories.all():
        reportes=RegistroUserStory.objects.filter(sprint=sprint, user_story=user_story)
        suma=0
        for reporte in reportes.all():
            suma+= reporte.horas_trabajadas

        reporte_total.append((user_story.nombre, user_story.estado_sprint, user_story.estimacion, suma,
                              user_story.get_prioridad_display))

    context = {"proyecto_id": proyecto_id, "reportes": reporte_total,"sprint_nombre":sprint.nombre,"fecha":fecha }

    html = render_to_string(path, context, request)
    io_bytes = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)

    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)
