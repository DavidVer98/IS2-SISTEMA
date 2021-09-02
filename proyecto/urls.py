from django.urls import path

from proyecto.views import proyecto, getMiembros, setMiembros, crearGrupo

urlpatterns = [

    path('<int:proyecto_id>/', proyecto, name="proyecto"),
    path('<int:proyecto_id>/miembros', getMiembros, name="miembros_proyecto"),
    path('<int:proyecto_id>/miembros/añadir', setMiembros, name="setMiembros_proyectos"),
    path('<int:proyecto_id>/roles/', crearGrupo, name="roles_proyecto"),

    # r'^/(?P<proyecto_id>\d+)/$' setMiembros '<int:proyecto_id>/miembros' proyect/1/miembros

]
