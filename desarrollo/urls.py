from django.urls import path

from desarrollo.views import desarrollo, productBacklog, crearUserStory

urlpatterns = [

    path('<int:proyecto_id>/desarrollo', desarrollo, name="desarrollo"),
    path('<int:proyecto_id>/desarrollo/productBacklog', productBacklog, name="productBacklog"),
    path('<int:proyecto_id>/desarrollo/productBacklog/crearUserStory', crearUserStory, name="crearUserStory"),

]
