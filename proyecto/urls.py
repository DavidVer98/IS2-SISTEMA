from django.urls import path

from proyecto.views import editar_rolmiembro, iniciar_proyecto, permisosRol
from proyecto.views import editarRol, eliminarRol, eliminarmiembro, eliminarProyecto
from proyecto.views import proyecto, getMiembros, setMiembros, crearGrupo, listarRol

urlpatterns = [



    path('<int:proyecto_id>/', proyecto, name="proyecto"),
    path('<int:proyecto_id>/miembros', getMiembros, name="miembros_proyecto"),
    path('<int:proyecto_id>/miembros/anadir', setMiembros, name="setMiembros_proyectos"),
    path('<int:proyecto_id>/roles/', crearGrupo, name="roles_proyecto"),
    path('<int:proyecto_id>/roles/listar', listarRol, name="listaRol"),

    path('<int:proyecto_id>/roles/<int:rol_id>/permisos', permisosRol, name='permisosRol'),
        path('<int:proyecto_id>/roles/<int:rol_id>/editar', editarRol, name='editarRol'),
    path('<int:proyecto_id>/roles/<int:rol_id>/eliminar', eliminarRol, name='eliminarRol'),
    path('<int:proyecto_id>/miembros/<int:miembro_id>/eliminar', eliminarmiembro, name="eliminarmiembro_proyecto"),
    path('<int:proyecto_id>/miembros/<int:miembro_id>/editar', editar_rolmiembro, name="editarmiembro-proyecto"),
    path('<int:proyecto_id>/eliminar', eliminarProyecto, name="eliminarProyecto"),
    path('<int:proyecto_id>/iniciar', iniciar_proyecto, name="iniciarProyecto"),
    # r'^/(?P<proyecto_id>\d+)/$' setMiembros '<int:proyecto_id>/miembros' proyect/1/miembros

]
