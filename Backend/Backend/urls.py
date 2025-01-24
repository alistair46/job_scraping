
from django.contrib import admin
from django.urls import path ,include
from Accounts import views

urlpatterns = [
    path('', views.Home ,name="HomePage"),
    path('admin/', admin.site.urls),
    path('api/', include("Accounts.urls")),
]

