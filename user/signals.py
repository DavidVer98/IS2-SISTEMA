from user.models import User


def populate_models(sender, **kwargs):
    from django.apps import apps
    from .apps import UserConfig
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    administradores, created = Group.objects.get_or_create(name='Administrador')
    #usuarios = Group.objects.get_or_create(name='Usuario')

    permissions=Permission.objects.filter(content_type__app_label=User._meta.app_label,
                              content_type__model=User._meta.model_name)
    administradores.permissions.add(*permissions)


