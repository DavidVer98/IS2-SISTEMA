from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from desarrollo.views import desarrollo, productBacklog, crearUserStory, editarUserStory, eliminarUserStory, \
    sprintPlanning, sprint_planning_estado, product_backlog_estado, asignarMiembroUS, planningPoker


class TestUrls(SimpleTestCase):

    def test_Desarrollo(self):
        url = reverse('desarrollo',kwargs={"proyecto_id":1})
        self.assertEqual(resolve(url).func,desarrollo,"No se utilizo el template de desarrollo")

    def test_sprintPlanning(self):
        url = reverse('sprintPlanning',kwargs={"proyecto_id":1})
        self.assertEqual(resolve(url).func,sprintPlanning,"No se utilizo el template de sprintPlanning")

    def test_asignarUS(self):
        url = reverse('asignarMiembroUS',kwargs={"proyecto_id":1, "user_story_id":1})
        self.assertEqual(resolve(url).func,asignarMiembroUS,"No se utilizo el template de asignarMiembroUS")

    def test_planningPoker(self):
        url = reverse('planningPoker',kwargs={"proyecto_id":1, "user_story_id":1})
        self.assertEqual(resolve(url).func,planningPoker,"No se utilizo el template de planningPoker")

    def test_productBacklog(self):
        url = reverse('productBacklog',kwargs={"proyecto_id":1})
        self.assertEqual(resolve(url).func,productBacklog,"No se utilizo el template de productBacklog")

    def test_crearUserStory(self):
        url = reverse('crearUserStory',kwargs={"proyecto_id":1})
        self.assertEqual(resolve(url).func,crearUserStory,"No se utilizo el template de crearUserStory")

    def test_editarUserStory(self):
        url = reverse('editarUserStory',kwargs={"proyecto_id":1, "user_story_id":1})
        self.assertEqual(resolve(url).func,editarUserStory,"No se utilizo el template de editarUserStory")

    def test_eliminarUserStory(self):
        url = reverse('eliminarUserStory',kwargs={"proyecto_id":1, "user_story_id":1})
        self.assertEqual(resolve(url).func,eliminarUserStory,"No se utilizo el template de eliminarUserStory")

    def test_sprintPlanningEstado(self):
        url = reverse('sprintPlanningEstado',kwargs={"proyecto_id":1, "user_story_id":1})
        self.assertEqual(resolve(url).func,sprint_planning_estado,"No se utilizo el template de seleccionar US")

    def test_ProductBacklogEstado(self):
        url = reverse('product_backlog_estado',kwargs={"proyecto_id":1, "user_story_id":1})
        self.assertEqual(resolve(url).func,product_backlog_estado,"No se utilizo el template de ver Product Backlog")

