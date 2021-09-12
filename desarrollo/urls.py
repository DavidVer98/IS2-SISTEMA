from django.urls import path

from desarrollo.views import desarrollo, productBacklog, crearUserStory, editarUserStory, eliminarUserStory

urlpatterns = [

    path('<int:proyecto_id>/desarrollo', desarrollo, name="desarrollo"),
    path('<int:proyecto_id>/desarrollo/productbacklog', productBacklog, name="productBacklog"),
    path('<int:proyecto_id>/desarrollo/productbacklog/crearUS', crearUserStory, name="crearUserStory"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/editar', editarUserStory, name="editarUserStory"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/eliminar', eliminarUserStory, name="eliminarUserStory"),
]
