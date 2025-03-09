from django.contrib import admin
from django.urls import path ,include
from Accounts import views

urlpatterns = [
    path('', views.Landing_Page ,name="LandingPage"),
    path('Home/', views.Home ,name="HomePage"),
    path('Aboutus/', views.Aboutus, name="About us"),
    path('admin/', admin.site.urls),
    path('api/', include("Accounts.urls")),
]

