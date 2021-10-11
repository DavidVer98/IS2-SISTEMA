from django.contrib.auth.models import Group
from django.test import TestCase
from desarrollo.models import UserStory, EstimacionPlanificada, Sprint, RegistroUserStory
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

        self.sprint= Sprint.objects.create(nombre="Sprint1",proyecto=self.proyecto,estado='Activo')

        self.registro=RegistroUserStory.objects.create(user_story=self.us, sprint=self.sprint, usuario="Developer1",detalles="Se registra el trabajo realizado",horas_trabajadas=5,horas_totales=20)
    def test_crearUS(self):
        self.assertEqual(self.us.proyecto.nombre_proyecto, 'Proyecto1',"El US no esta en el proyecto 1")

    def test_estimacion(self):
        self.assertEqual((self.estimacion.estimacion_scrum+self.estimacion.estimacion_miembro)/2,self.us.estimacion,"La estimacion no se cargo correctamente")

    """Para iteracion 4"""

    def test_sprintNombre(self):
        self.assertEqual(self.sprint.nombre,"Sprint1","El nombre del sprint no se guardo correctamente")

    def test_Sprintproyecto(self):
        self.assertEqual(self.sprint.proyecto.nombre_proyecto,'Proyecto1',"El sprint no pertenece al proyecto 1")

    def test_sprintEstado(self):
        self.assertEqual(self.sprint.estado,'Activo',"El estado no se cargo correctamente")

    def test_registroUS(self):
        self.assertEqual(self.registro.user_story.nombre, "US1","El registro no es del US1")

    def test_registroSprint(self):
        self.assertEqual(self.registro.sprint.nombre,"Sprint1","El registro no se esta realizando sobre el Sprint1")

    def test_registroUser(self):
        self.assertEqual(self.registro.usuario,"Developer1","El registro no fue realizado por el Developer1")

    def test_registrodetalles(self):
        self.assertTrue(self.registro.detalles!=None,"La descripcion en el registro esta vacia")

    def test_registroHT(self):
        self.assertEqual(self.registro.horas_trabajadas,5,"Las horas trabajadas no se cargaron corretamente")

    def test_registroHtotal(self):
        self.assertEqual(self.registro.horas_totales,20,"Las horas totales no se cargaron correctamente")
