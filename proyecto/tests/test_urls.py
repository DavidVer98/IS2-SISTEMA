from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from proyecto.views import proyecto, getMiembros, setMiembros, crearGrupo, listarRol, editarRol, eliminarRol, \
    eliminarmiembro, editar_rolmiembro, cancelarProyecto


class TestUrls(SimpleTestCase):

    def test_proyecto_url(self):
        url = reverse('proyecto', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, proyecto)

    def test_getMiembros_url(self):
        url = reverse('miembros_proyecto', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, getMiembros)

    def test_agregarMiembros_url(self):
        url = reverse('setMiembros_proyectos', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, setMiembros)

    def test_crearRol(self):
        url = reverse('roles_proyecto', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, crearGrupo)

    def test_listarRol(self):
        url = reverse('listaRol', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, listarRol)

    def test_editarRol(self):
        url = reverse('editarRol', kwargs={"proyecto_id": 1, "rol_id": 1})
        self.assertEqual(resolve(url).func, editarRol)

    def test_eliminarRol(self):
        url = reverse('eliminarRol', kwargs={"proyecto_id": 1, "rol_id": 1})
        self.assertEqual(resolve(url).func, eliminarRol)

    def test_eliminarMiembro(self):
        url = reverse('eliminarmiembro_proyecto', kwargs={"proyecto_id": 1, "miembro_id": 2})
        self.assertEqual(resolve(url).func, eliminarmiembro)

    def test_editarMiembro(self):
        url = reverse('editarmiembro-proyecto', kwargs={"proyecto_id": 1, "miembro_id": 2})
        self.assertEqual(resolve(url).func, editar_rolmiembro)

    def test_cancelarproyecto_url(self):
        url = reverse('cancelarProyecto', kwargs={"proyecto_id": 1})
        self.assertEqual(resolve(url).func, cancelarProyecto)
