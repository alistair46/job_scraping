from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (UserResistrationSerializer ,UserLoginSerializers ,
                          ProfileSerializers ,ForgotUserPasswordSerializer ,
                          SendPasswordResetEmailSerializer,UserPasswordRestSerializer)
from rest_framework import status
from django.contrib.auth import authenticate
from Accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


#To generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh),'access': str(refresh.access_token),}


class UserResistrationView(APIView):
    renderer_classes = [UserRenderer]  # For frontend to show error messages
# Render the signup form
    def get(self, request):
        return render(request, "Accounts/signup.html")
# Handle form submission
    def post(self, request, format=None):
        serializer = UserResistrationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)  # Generate token for the user
# Redirect to login page for browser-based requests
            if request.headers.get('Content-Type') != 'application/json':
                return redirect('login')  
# Return API response for JSON requests
            return Response({'token': token, 'message': 'Registration Successful!!'}, status=status.HTTP_201_CREATED)
# Handle validation errors
        if request.headers.get('Content-Type') != 'application/json':
            return render(request, "Accounts/signup.html", {"errors": serializer.errors})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes=[UserRenderer] # for frontend to show error
    def get(self,request):
        return render (request, "Accounts/login.html")
    def post(self,request,format=None):
        serializer=UserLoginSerializers(data=request.data)
# Here we are authenitcate user using django authenticate method  where we pass email and password to get verified
        if (serializer.is_valid(raise_exception=True)):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
# Redirect to dashboard for browser-based requests
                if request.headers.get('Content-Type') != 'application/json':
                    return redirect('HomePage') 
# Return API response for JSON requests
                return Response(
                    {'token': token, 'message': 'Login Successful!!'},status=status.HTTP_200_OK)
# Invalid credentials
            if request.headers.get('Content-Type') != 'application/json':
                return render(request, "Accounts/login.html", {
                    "errors": {"non_field_errors": ["Email or password is not valid"]}})
            return Response(
                {'errors': {'non_field_errors': ['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
# Handle serializer errors
        if request.headers.get('Content-Type') != 'application/json':
            return render(request, "Accounts/login.html", {"errors": serializer.errors})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
class ProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer= ProfileSerializers(request.user)
        return Response (serializer.data,status=status.HTTP_200_OK)
    
# Forgot password 
class ForgotUserPasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer =ForgotUserPasswordSerializer(data=request.data ,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'password change Sucessfull !!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#Reset password via email
class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer= SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'password reset email send please check your email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserPasswordRestview(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,token,uid,format=None):
        serializer=UserPasswordRestSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'password reset sucessfull !!!.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def Home(request):
    return render(request, "Accounts/home.html")
    