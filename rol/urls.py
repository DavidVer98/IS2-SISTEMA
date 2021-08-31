from django.urls import path
from .views  import crearGrupo

urlpatterns = [

    path('crear/',crearGrupo ),

]
