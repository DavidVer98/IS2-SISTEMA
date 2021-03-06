from django.urls import path

from desarrollo.views import desarrollo, productBacklog, crearUserStory, editarUserStory, eliminarUserStory, \
    sprintPlanning, sprint_planning_estado, product_backlog_estado, asignarMiembroUS, planningPoker, sprintBacklog, \
    iniciarSprint, estadoUS, registrarUS, registroUSActual, terminarSprint, reasignarMiembroUS, registroUserStories, \
    registroSprints, burndown_chart, chart_sprint_activo, historial_sprint, historial_sprint_backlog, \
    reporte_product_backlog, reporte_sprint_backlog, reporte_sprint

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
    path('<int:proyecto_id>/desarrollo/sprintplanning/<int:user_story_id>/reasignarmiembro', reasignarMiembroUS, name="reasignarMiembroUS"),
    path('<int:proyecto_id>/desarrollo/sprintplanning/<int:user_story_id>/planningpoker', planningPoker, name="planningPoker"),
    path('<int:proyecto_id>/desarrollo/productbacklog', productBacklog, name="productBacklog"),
    path('<int:proyecto_id>/desarrollo/productbacklog/crearUS', crearUserStory, name="crearUserStory"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/editar', editarUserStory, name="editarUserStory"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/eliminar', eliminarUserStory, name="eliminarUserStory"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/seleccionar', sprint_planning_estado, name="sprintPlanningEstado"),
    path('<int:proyecto_id>/desarrollo/productbacklog/<int:user_story_id>/seleccionar/productbacklog', product_backlog_estado, name="product_backlog_estado"),
    path('<int:proyecto_id>/desarrollo/registros', registroSprints, name="registroSprints"),
    path('<int:proyecto_id>/desarrollo/registros/<int:sprint_id>', registroUserStories, name="registroUserStories"),
    path('<int:proyecto_id>/desarrollo/historial/chart/<int:sprint_id>', burndown_chart, name="burndown_chart"),
    path('<int:proyecto_id>/desarrollo/chart', chart_sprint_activo, name="chart_sprint_activo"),
    path('<int:proyecto_id>/desarrollo/historial/<int:sprint_id>', historial_sprint, name="historial_sprint"),
    path('<int:proyecto_id>/desarrollo/historial/sprintBacklog/<int:sprint_id>', historial_sprint_backlog, name="historial_sprint_backlog"),
    path('<int:proyecto_id>/desarrollo/productbacklog/reporte', reporte_product_backlog, name="reporte_product_backlog"),
    path('<int:proyecto_id>/desarrollo/sprintbacklog/reporte', reporte_sprint_backlog, name="reporte_sprint_backlog"),
    path('<int:proyecto_id>/desarrollo/historial/<int:sprint_id>/reporte', reporte_sprint, name="reporte_sprint"),
]



