from django.shortcuts import render

# Create your views here.
def activar(request):
    return render(request, 'user/activar.html')