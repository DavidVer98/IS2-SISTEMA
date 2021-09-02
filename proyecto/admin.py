from django.contrib import admin
from proyecto.models import Proyecto, Miembro, Rol

admin.site.register(Proyecto)

@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):

    list_display = ('pk','miembro', 'proyectos','rol')
    list_display_links =('miembro','pk')
