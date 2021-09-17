from django.contrib.auth.models import Group
from django.test import TestCase
from desarrollo.models import UserStory, EstimacionPlanificada
from proyecto.models import Proyecto, Miembro, Rol
from user.models import User

class TestModels(TestCase):

    def setUp(self):
        self.user=User.objects.create(username='scrum',email= 'scrumaster@gmail.com', password='scrummaster', estaActivado=True)
        self.user2=User.objects.create(username='developer',email= 'developer@gmail.com', password='developer', estaActivado=True)
        self.proyecto=Proyecto.objects.create(nombre_proyecto='Proyecto1',scrum_master=self.user,estado='PENDIENTE',fecha_inicio='2022-03-03')
        grupo=Group.objects.create()
        self.rol=Rol.objects.create(nombre="Developer",group=grupo)
        self.miembro=Miembro.objects.create(miembro=self.user2,proyectos=self.proyecto,rol=self.rol,produccion_por_semana=15)

        self.us = UserStory.objects.create(proyecto=self.proyecto, miembro_asignado=self.user2, nombre="US1",
                                           descripcion="Test de User Story", estado_sprint="TO_DO", estimacion=0,
                                           prioridad=1, estado_desarrollo="EN PRODUCT BACKLOG")
        self.estimacion = EstimacionPlanificada.objects.create(user_story=self.us, estimacion_scrum=30,
                                                               estimacion_miembro=15)
        self.us.estimacion=(self.estimacion.estimacion_scrum+self.estimacion.estimacion_miembro)/2
    def test_crearUS(self):
        self.assertEqual(self.us.proyecto.nombre_proyecto, 'Proyecto1',"El US no esta en el proyecto 1")

    def test_estimacion(self):
        self.assertEqual((self.estimacion.estimacion_scrum+self.estimacion.estimacion_miembro)/2,self.us.estimacion,"La estimacion no se cargo correctamente")