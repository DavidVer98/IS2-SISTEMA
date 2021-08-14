from allauth.account.views import logout
from django.shortcuts import render, redirect


# Create your views here.
def login_views (request):
    return render(request,'user/login.html')

def home(request):
    return render(request,'user/index.html')

def logout_view(request):
    logout(request)
    return redirect('login')