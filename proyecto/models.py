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
    developer_perm = [
        ("VER_PROYECTO"),
        ("VER_MIEMBRO"),
        ("VER_ROL"),
        ("VER_PRODUCT_BACKLOG"),
        ("VER_SPRINT_PLANNING"),
        ("ESTIMAR_USER_STORY"),
        ("VER_SPRINT_BACKLOG"),
        ("CREAR_REGISTRO_US"),
        ("CAMBIO_ESTADO_US"),
        ("VER_REGISTRO_US"),

    ]
    productowner_perm = [
        ("VER_PROYECTO"),
        ("VER_MIEMBRO"),
        ("VER_ROL"),
        ("VER_PRODUCT_BACKLOG"),
        ("VER_SPRINT_BACKLOG"),
        ("VER_REGISTROS"),

    ]
    def __str__(self):
        return self.nombre

    def permdeveloper(cls):
        return cls.developer_perm
    def permproductowner(cls):
        return cls.productowner_perm
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
        import random

        # se extraen los miembros del proyecto con el rol
        miembros_con_el_rol = Miembro.objects.filter(rol=self)

        # Se estrae el grupo del rol y se elimina
        nombre_grupo=self.group.name
        grupo_anterior = self.group
        grupo_anterior.name=str(random.getrandbits(60))
        grupo_anterior.save()


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
        grupo_anterior.delete()
    @classmethod
    def crearScrum(cls, proyecto_id):
        permissions = Permission.objects.filter(content_type__app_label='proyecto', content_type__model='proyecto')
        proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
        scrum = 'Scrum Master'
        return cls.crear(scrum, permissions, proyecto_actual)

    @classmethod
    def rolespordefecto(cls, proyecto_id):
        permissions = Permission.objects.filter(content_type__app_label='proyecto', content_type__model='proyecto')
        permissionsdev= permissions.filter(codename__in=cls.permdeveloper(cls))
        permissionsproductowner = permissions.filter(codename__in=cls.permproductowner(cls))
        proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
        cls.crear('Developer',permissionsdev, proyecto_actual)
        cls.crear('Product Owner', permissionsproductowner, proyecto_actual)
        return  cls.crear('Scrum Master', permissions, proyecto_actual)

class Proyecto(models.Model):
    """
     **Proyecto:**
     03/09/2021
     Model de los datos necesarios para el manejo de un Proyecto

    """
    PENDIENTE='PENDIENTE'
    ACTIVO='ACTIVO'
    CANCELADO='CANCELADO'
    ESTADO_PROYECTO_CHOICES = [
        ('P', 'PENDIENTE'),
        ('A', 'ACTIVO'),
        ('C', 'CANCELADO'),
    ]
    nombre_proyecto = models.CharField(max_length=50)
    scrum_master = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=ESTADO_PROYECTO_CHOICES, default=PENDIENTE)
    fecha_inicio = models.DateField()
    roles = models.ManyToManyField(Rol)
    descripcion = models.TextField(max_length=800)
    duracion_semanal_sprint= models.PositiveIntegerField(default=2)
    duracion_semanal_sprint_actual = models.FloatField(default=2.0)
    def iniciar_proyecto(self):
        self.estado = self.ACTIVO
        self.save()

    def setScrum(self, user, rol):
        miembro = Miembro.objects.create(proyectos=self, miembro=user, rol=rol)
        miembro.save()
        user.groups.add(rol.group)

    def reasignarScrum(self, scrum_nuevo):
        miembro = Miembro.objects.get(proyectos=self, miembro=self.scrum_master.pk)
        # si el nuevo scrum es parte del proyecto, se borra la relacion anterior
        if Miembro.objects.filter(proyectos=self, miembro=scrum_nuevo).exists():
            miembro_existente=Miembro.objects.get(proyectos=self, miembro=scrum_nuevo)
            grupo_rol_de_miembro=miembro_existente.rol.group
            miembro_existente.miembro.groups.remove(grupo_rol_de_miembro)
            miembro_existente.delete()
        grupo_rol = miembro.rol.group
        scrum_anterior = miembro.miembro
        # se remueve del grupo scrum master al scrum master anterior
        scrum_anterior.groups.remove(grupo_rol)
        #se asigna al nuevo scrum master como miembro del proyecto
        miembro.miembro=scrum_nuevo
        # se asigna al nuevo scrum master al grupo scrum master
        miembro.miembro.groups.add(grupo_rol)
        miembro.save()
        self.scrum_master = scrum_nuevo
        self.save()


    def agregarRol(self, rol):
        self.roles.add(rol)
        return self.roles

    def __str__(self):
        return self.nombre_proyecto

    class Meta:
        default_permissions = ()
        permissions = [
            ("VER_PROYECTO", "Puede visualizar el proyecto en la lista de proyectos"),
            ("INICIAR_PROYECTO", "Puede iniciar la ejecucion de un proyecto"),
            ("CANCELAR_PROYECTO", "Puede cancelar el proyecto"),

            ("VER_MIEMBRO", "Puede ver la lista de miembros del proyecto"),
            ("AGREGAR_MIEMBRO", "Puede agregar miembros al proyecto"),
            ("EDITAR_MIEMBRO", "Puede editar roles de miembros del proyecto"),
            ("ELIMINAR_MIEMBRO", "Puede eliminar miembros del proyecto"),

            ("VER_ROL", "Puede ver lista de roles del proyecto"),
            ("CREAR_ROL", "Puede crear roles del proyecto"),
            ("EDITAR_ROL", "Puede editar roles del proyecto"),
            ("ELIMINAR_ROL", "Puede eliminar roles del proyecto"),

            ("VER_PRODUCT_BACKLOG", "Puede visualizar la seccion de product backlog"),
            ("CREAR_USER_STORY", "Puede crear user stories"),
            ("EDITAR_USER_STORY", "Puede editar user stories"),
            ("ELIMINAR_USER_STORY", "Puede eliminar user stories"),

            ("VER_SPRINT_PLANNING", "Puede ver la seccion de planificacion de sprint"),
            ("PLANIFICAR_SPRINT", "Puede planificar el siguiente sprint"),
            ("ESTIMAR_USER_STORY", "Puede estimar los user stories en la planificacion"),

            ("INICIAR_SPRINT", "Puede iniciar un sprint "),
            ("TERMINAR_SPRINT", "Puede terminar un sprint "),

            ("VER_SPRINT_BACKLOG", "Puede ver la seccion de sprint backlog"),
            ("REASIGNAR_MIEMBRO", "Puede reasignar miembros en el sprint backlog"),
            ("VER_REGISTRO_US", "Puede ver los registros sobre un user story"),
            ("CREAR_REGISTRO_US", "Puede crear registros de user story"),
            ("CAMBIO_ESTADO_US", "Puede cambiar los estados de us en la tabla kanban"),

            ("VER_REGISTROS", "Puede ver todos los registros creados en un proyecto"),
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
    produccion_por_semana = models.IntegerField("Horas de produccion semanal",default=0, blank=True ,null=False )

    def __str__(self):
        return self.miembro.username
