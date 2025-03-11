from django.contrib import admin
from django.urls import path ,include
from Accounts import views as accounts_view
# from jobs import views as job_view
from jobs.views import JobCompareView

urlpatterns = [
    path('', JobCompareView.as_view() ,name="LandingPage"),
    path('Home/', accounts_view.Home ,name="HomePage"),
    path('Aboutus/', accounts_view.Aboutus, name="About us"),
    path('admin/', admin.site.urls),
    path('api/', include("Accounts.urls")),
]

