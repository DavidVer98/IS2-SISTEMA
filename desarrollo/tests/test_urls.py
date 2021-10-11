from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from desarrollo.views import desarrollo, productBacklog, crearUserStory, editarUserStory, eliminarUserStory, \
    sprintPlanning, sprint_planning_estado, product_backlog_estado, asignarMiembroUS, planningPoker, registrarUS, \
    registroUSActual,iniciarSprint, terminarSprint, sprintBacklog, estadoUS, reasignarMiembroUS, registroSprints, \
    registroUserStories


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

    """ Para iteracion 4"""

    def test_registrarUS(self):
        url = reverse('registroUS', kwargs={"proyecto_id": 1, "user_story_id": 1})
        self.assertEqual(resolve(url).func, registrarUS, "No se utilizo el template de registros")

    def test_registroUS(self):
        url = reverse('registroUSActual', kwargs={"proyecto_id": 1, "user_story_id": 1})
        self.assertEqual(resolve(url).func, registroUSActual, "No se utilizo el template de registros")

    def test_iniciarSprint(self):
        url = reverse('iniciarSprint', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, iniciarSprint, "No se utilizo el template iniciar Sprint")

    def test_terminarSprint(self):
        url = reverse('terminarSprint', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, terminarSprint, "No se utilizo el template de terminar sprint")

    def test_sprintBacklog(self):
        url = reverse('sprintBacklog', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, sprintBacklog, "No se utilizo el template de sprintBacklog")

    def test_estadoUS(self):
        url = reverse('estadoUS', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, estadoUS, "No se utilizo el template de estadoUS")

    def test_reasignarMiembroUS(self):
        url = reverse('reasignarMiembroUS', kwargs={"proyecto_id": 1, "user_story_id": 1})
        self.assertEqual(resolve(url).func, reasignarMiembroUS, "No se utilizo el template de reasignarMiembroUS")

    def test_registroSprints(self):
        url = reverse('registroSprints', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, registroSprints, "No se utilizo el template de registroSprints")

    def test_registroUserStories(self):
        url = reverse('registroUserStories', kwargs={"proyecto_id": 1,"sprint_id":1})
        self.assertEqual(resolve(url).func, registroUserStories, "No se utilizo el template de registroSprints")




