from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def Home(request):
    return render(request, "Accounts/home.html")
    #return HttpResponse("You're looking at question %s.")


def Signup(request):
    pass

def login(request):
    pass