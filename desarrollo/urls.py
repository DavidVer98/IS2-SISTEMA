from django.urls import path

from desarrollo.views import desarrollo

urlpatterns = [

    path('<int:proyecto_id>/desarrollo',desarrollo, name="desarrollo"),

]
