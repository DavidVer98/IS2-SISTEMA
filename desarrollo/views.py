from django.shortcuts import render

# Create your views here.
from proyecto.models import Proyecto


def desarrollo(request, proyecto_id):
    proyecto_actual = Proyecto.objects.get(pk=proyecto_id)
    proyecto_actual.iniciar_proyecto()
    context = {"proyecto_id": proyecto_id, "proyecto": proyecto_actual}
    return render(request, "desarrollo/desarrollo.html", context)
