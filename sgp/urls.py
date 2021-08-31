"""sgp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from home.views import home, listarUsuarios, eliminar, editar
from oauth_app.views import login_views, logout_view
from proyecto.views import listarProyectos, editarProyecto, crearProyecto
from user.views import activar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login/', login_views, name="login"),
    path('logout/', logout_view, name="logout"),
    path('home/', home, name="home"),
    path('home/usuarios', listarUsuarios, name="listaUsuarios"),
    path('', TemplateView.as_view(template_name="user/login.html")),
    path("eliminar/<int:user_id>/", eliminar, name="eliminar"),
    path("editar/<int:user_id>/", editar, name="editar"),
    path("home/proyectos/", listarProyectos, name="listarProyectos"),
    path("home/proyectos/editar/<int:proyecto_id>/", editarProyecto, name="editarProyecto"),
    path("home/proyectos/crear", crearProyecto, name="crearProyecto"),
    path("user/activar/",activar,name="activar"),
    path("rol/",include("rol.urls"))
]
