from allauth.account.views import logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


# Create your views here.
def login_views (request):
    return render(request,'user/login.html')


def logout_view(request):
    auth_logout(request)
    logout(request)
    return redirect('login')