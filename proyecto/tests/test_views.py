from django.test import TestCase, Client,override_settings
from proyecto.views import *
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
#from user.models import User
from proyecto.models import Rol, Proyecto, Miembro

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        User=get_user_model()
        self.user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='johnpassword',estaActivado=True)
        self.listaurl=reverse('listarProyectos')

    def test_ListaProyecto(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(self.listaurl)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home/listarProyectos.html')

    def testLogin(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


