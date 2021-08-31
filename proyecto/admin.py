from django.contrib import admin

# Register your models here.
from proyecto.models import Proyecto, Miembro

admin.site.register(Proyecto)
admin.site.register(Miembro)