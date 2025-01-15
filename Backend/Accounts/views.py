from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def Home(request):
    return render(request, "Accounts/home.html")
    


def Signup(request):
    return render(request, "Accounts/signup.html")

def login(request):
    return render(request, "Accounts/login.html")