from django.test import TestCase
from proyecto.models import Rol, Proyecto, Miembro
from user.models import User
from django.contrib.auth.models import Group


class TestModels(TestCase):

    def setUp(self):
        self.user=User.objects.create(username='scrum',email= 'scrumaster@gmail.com', password='scrummaster', estaActivado=True)
        id=self.user.pk
        self.proyecto=Proyecto.objects.create(nombre_proyecto='Proyecto1',scrum_master=self.user,estado='PENDIENTE',fecha_inicio='2022-03-03')

    def test_PruebaProyecto(self):

        self.assertEqual(self.proyecto.scrum_master.username,'scrum')