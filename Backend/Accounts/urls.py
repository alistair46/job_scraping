from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home ,name="HomePage"),
    path('login/', views.login ,name="loginPage"),
    path('Signup/', views.Signup ,name="SignupPage"),
]