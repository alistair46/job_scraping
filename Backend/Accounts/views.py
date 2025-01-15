from django.shortcuts import render
import requests

# Create your views here.

def Home(request):
    return render( request, 'Accounts/home.html')


def Signup(requests):
    pass

def login(requests):
    pass