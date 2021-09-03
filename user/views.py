from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required(login_url='/login')
def activar(request):
    """
        Vista desplegada a usuarios no activados  03/09/21
    """
    return render(request, 'user/activar.html')