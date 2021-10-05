from django.urls import path

from desarrollo.views import desarrollo, productBacklog, crearUserStory, editarUserStory, eliminarUserStory, \
    sprintPlanning, sprint_planning_estado, product_backlog_estado, asignarMiembroUS, planningPoker, sprintBacklog, \
    iniciarSprint, estadoUS, registrarUS, registroUSActual, terminarSprint

urlpatterns = [

    path('<int:proyecto_id>/desarrollo', desarrollo, name="desarrollo"),
    path('<int:proyecto_id>/desarrollo/<int:user_story_id>/registrar', registrarUS, name="registroUS"),
    path('<int:proyecto_id>/desarrollo/<int:user_story_id>/registro/', registroUSActual, name="registroUSActual"),
    path('<int:proyecto_id>/desarrollo/iniciarsprint', iniciarSprint, name="iniciarSprint"),
    path('<int:proyecto_id>/desarrollo/terminarsprint', terminarSprint, name="terminarSprint"),
    path('<int:proyecto_id>/desarrollo/sprintbacklog', sprintBacklog, name="sprintBacklog"),
    path('<int:proyecto_id>/desarrollo/sprintbacklog/estadous', estadoUS, name="estadoUS"),
    path('<int:proyecto_id>/desarrollo/sprintplanning', sprintPlanning, name="sprintPlanning"),
    path('<int:proyecto_id>/desarrollo/sprintplanning/<int:user_story_id>/asignarmiembro', asignarMiembroUS, name="asignarMiembroUS"),
    path('<int:proyecto_id>/desarrollo/sprintplanning/<int:user_story_id>/planningpoker', planningPoker, name="planningPoker"),
    path('<int:proyecto_id>/desarrollo/productbacklog', productBacklog, name="productBacklog"),
    path('<int:proyecto_id>/desarrollo/productbacklog/crearUS', crearUserStory, name="crearUserStory"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/editar', editarUserStory, name="editarUserStory"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/eliminar', eliminarUserStory, name="eliminarUserStory"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/seleccionar', sprint_planning_estado, name="sprintPlanningEstado"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/seleccionar/productbacklog', product_backlog_estado, name="product_backlog_estado"),
]



