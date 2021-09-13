from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from proyecto.models import Proyecto, Miembro, Rol



class AuthorAdmin(GuardedModelAdmin):
    pass

admin.site.register(Proyecto, AuthorAdmin)


@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):

    list_display = ('pk','miembro', 'proyectos','rol')
    list_display_links =('miembro','pk')
