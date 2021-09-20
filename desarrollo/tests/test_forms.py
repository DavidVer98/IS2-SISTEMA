from django.http import HttpRequest
from django.test import TestCase
from django.contrib.auth.models import Group
from desarrollo.forms import UserStoryForms,UserStoryMiembroForms,PlanningPokerForms
from desarrollo.models import UserStory, EstimacionPlanificada
from proyecto.models import Proyecto, Miembro, Rol
#from user.models import User
from django.contrib.auth import get_user_model


class TestForms(TestCase):



    def test_USF(self):
        User=get_user_model()

        user2 = User.objects.create_user(username='developer', email='developer@gmail.com', password='developer',
                                         estaActivado=True)
        proyecto = Proyecto.objects.create(nombre_proyecto='Proyecto1', scrum_master=user2, estado='PENDIENTE',
                                                fecha_inicio='2022-03-03')
        us = UserStory.objects.create(proyecto=proyecto, miembro_asignado=user2, nombre="US1",
                                           descripcion="Test de User Story", estado_sprint="TO_DO", estimacion=0,
                                           prioridad=1, estado_desarrollo='EN PRODUCT BACKLOG')
        estimacion = EstimacionPlanificada.objects.create(user_story=us, estimacion_scrum=30,
                                                               estimacion_miembro=15)

        request = HttpRequest()
        request.POST={
            "nombre":"US1",
            "descripcion":"Test de User Story",
            "prioridad":1,

        }

        form = UserStoryForms(request.POST or None)
        self.assertTrue(form.is_valid(),"El formulario no es valido")

    def test_UserStoryMiembroForms(self):

        User = get_user_model()

        user2 = User.objects.create_user(username='developer', email='developer@gmail.com', password='developer',
                                         estaActivado=True)
        proyecto = Proyecto.objects.create(nombre_proyecto='Proyecto1', scrum_master=user2, estado='PENDIENTE',
                                           fecha_inicio='2022-03-03')
        us = UserStory.objects.create(proyecto=proyecto, miembro_asignado=user2, nombre="US1",
                                      descripcion="Test de User Story", estado_sprint="TO_DO", estimacion=0,
                                      prioridad=1, estado_desarrollo='EN PRODUCT BACKLOG')
        estimacion = EstimacionPlanificada.objects.create(user_story=us, estimacion_scrum=30,
                                                          estimacion_miembro=15)

        request = HttpRequest()
        request.POST = {
            "miembro_asignado": user2,

        }
        form = UserStoryMiembroForms(request.POST or None)
        self.assertTrue(form.is_valid(), "El formulario no es valido")

    def test_planningpokerFrom(self):
        request = HttpRequest()
        request.POST = {
            "estimacion_miembro":5
        }
        form=PlanningPokerForms(request.POST or None)
        self.assertTrue(form.is_valid(), "El formulario no es valido")




