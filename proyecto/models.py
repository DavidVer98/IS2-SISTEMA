from django.db import models
from django.contrib.auth.models import Group, Permission
from guardian.shortcuts import assign_perm

from user.models import User


class Rol(models.Model):
    """
    **Rol:**
    03/09/2021
    Modelo de Rol que maneja el nombre del rol y enlaza con el groups de django

    """
    nombre = models.TextField(max_length=50)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    @classmethod
    def crear(cls, name, permissions, proyecto_actual):
        #Para permitir creacion de roles con igual nombre pero con nombre de group distinto
        name_group=name + str(proyecto_actual.pk)
        grupo = Group.objects.create(name=name_group)

        rol = cls(nombre=name, group=grupo)
        for perm in permissions:
            assign_perm(perm, rol.group, proyecto_actual)
        rol.save()
        proyecto_actual.agregarRol(rol)
        return rol

    def editar(self, permisos_elegidos, proyecto_id):
        # Se trae el modelo del rol


        # se extraen los miembros del proyecto con el rol
        miembros_con_el_rol = Miembro.objects.filter(rol=self)

        # Se estrae el grupo del rol y se elimina
        nombre_grupo=self.group.name
        grupo_anterior = self.group
        grupo_anterior.delete()

        # se crea nuevo grupo
        self.group = Group.objects.create(name=nombre_grupo)

        # SE NECESITA EL PROYECTO_ID PARA ASIGNAR LOS NUEVOS PERMISOS
        proyecto_actual = Proyecto.objects.get(pk=proyecto_id)

        # se asignan los nuevos permisos al grupo
        for perm in permisos_elegidos:
            assign_perm(perm, self.group, proyecto_actual)
        # se agregan a los miembros al nuevo grupo si es que alguno existe
        if miembros_con_el_rol.exists():
            for miembro in miembros_con_el_rol:
                miembro.miembro.groups.add(self.group)

        self.group.save()
        self.save()
        proyecto_actual.roles.add(self)
        proyecto_actual.save()

    @classmethod
    def crearScrum(cls, proyecto_id):
        permissions = Permission.objects.filter(content_type__app_label='proyecto', content_type__model='proyecto')
        proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
        scrum = 'Scrum Master'
        return cls.crear(scrum, permissions, proyecto_actual)


class Proyecto(models.Model):
    """
     **Proyecto:**
     03/09/2021
     Model de los datos necesarios para el manejo de un Proyecto

    """
    nombre_proyecto = models.CharField(max_length=50)
    scrum_master = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, default="PENDIENTE")
    fecha_inicio = models.DateField()
    roles = models.ManyToManyField(Rol)

    def iniciar_proyecto(self):
        self.estado = "ACTIVO"
        self.save()

    def setScrum(self, user, rol):
        miembro = Miembro.objects.create(proyectos=self, miembro=user, rol=rol)
        miembro.save()
        user.groups.add(rol.group)

    def agregarRol(self, rol):
        self.roles.add(rol)
        return self.roles

    def __str__(self):
        return self.nombre_proyecto

    class Meta:
        default_permissions = ()
        permissions = [
            ("VER_PROYECTO", "Puede visualizar el proyecto en la lista de proyectos"),
            ("CREAR_PROYECTO", "Puede crear proyectos"),
            ("EDITAR_PROYECTO", "Puede editar configuraciones basicas del proyecto"),
            ("INICIAR_PROYECTO", "Puede iniciar la ejcucion de un proyecto"),
            ("ELIMINAR_PROYECTO", "Puede elimiar proyectos"),
            ("VER_MIEMBRO", "Puede ver la lista de miembros del proyecto"),
            ("AGREGAR_MIEMBRO", "Puede agregar miembros al proyecto"),
            ("EDITAR_MIEMBRO", "Puede agregar miembros al proyecto"),
            ("ELIMINAR_MIEMBRO", "Puede eliminar miembros del proyecto"),
            ("VER_ROL", "Puede ver lista de roles del proyecto"),
            ("CREAR_ROL", "Puede crear roles del proyecto"),
            ("EDITAR_ROL", "Puede crear roles del proyecto"),
            ("ELIMINAR_ROL", "Puede eliminar roles del proyecto"),
        ]


class Miembro(models.Model):
    """
        **Miembro:**
        03/09/2021
        Model que representa la relacion de un usuario, un proyecto y un rol

    """
    miembro = models.ForeignKey(User, on_delete=models.PROTECT)
    proyectos = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    def __str__(self):
        return self.miembro.username
