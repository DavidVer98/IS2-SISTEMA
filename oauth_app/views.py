from allauth.account.views import logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


# Create your views here.
def login_views (request):
    """
        Vista utilizada para retornar al login  03/09/21
    """
    return render(request,'user/login.html')


def logout_view(request):
    """
        Vista utilizada para cerrar sesion  03/09/21
    """
    auth_logout(request)
    logout(request)
    return redirect('login')