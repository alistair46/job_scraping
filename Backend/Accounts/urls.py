from Accounts.views import UserResistrationView ,UserLoginView ,ProfileView ,ForgotUserPasswordView ,SendPasswordResetEmailView,UserPasswordRestview
from django.urls import path 

urlpatterns = [
    path('register/', UserResistrationView.as_view() , name='register' ),
    path('login/', UserLoginView.as_view() , name='login' ),
    path('profile/', ProfileView.as_view() , name='profile' ),
    path('ForgotPassword/', ForgotUserPasswordView.as_view() , name='Forgot Password' ),
    path('ResetMail/', SendPasswordResetEmailView.as_view() , name='ResetMail' ),
    path('ResetPassword/<uid>/<token>/', UserPasswordRestview.as_view() , name='Reset Password' ),
    
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.Home ,name="HomePage"),
#     path('login/', views.login ,name="loginPage"),
#     path('signup/', views.Signup ,name="SignupPage"),
# ]
