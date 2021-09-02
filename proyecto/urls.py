from django.urls import path

from proyecto.views import proyecto, getMiembros, setMiembros, crearGrupo, eliminarmiembro

urlpatterns = [

    path('<int:proyecto_id>/', proyecto, name="proyecto"),
    path('<int:proyecto_id>/miembros', getMiembros, name="miembros_proyecto"),
    path('<int:proyecto_id>/miembros/añadir', setMiembros, name="setMiembros_proyectos"),
    path('<int:proyecto_id>/roles/', crearGrupo, name="roles_proyecto"),
    path('<int:proyecto_id>/miembros/<int:miembro_id>/eliminar', eliminarmiembro, name="eliminarmiembro_proyecto"),
    # r'^/(?P<proyecto_id>\d+)/$' setMiembros '<int:proyecto_id>/miembros' proyect/1/miembros

]
