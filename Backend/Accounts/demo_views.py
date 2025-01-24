from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    UserResistrationSerializer, 
    UserLoginSerializers, 
    ProfileSerializers, 
    ForgotUserPasswordSerializer, 
    SendPasswordResetEmailSerializer, 
    UserPasswordRestSerializer
)
from rest_framework import status
from django.contrib.auth import authenticate
from Accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# To generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

# Helper function for handling form-based responses
def handle_form_response(request, template, errors=None):
    if request.headers.get('Content-Type') != 'application/json':
        return render(request, template, {"errors": errors})
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# Helper function to handle redirects for browser requests
def handle_browser_redirect(request, redirect_url):
    if request.headers.get('Content-Type') != 'application/json':
        return redirect(redirect_url)
    return None


class UserResistrationView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request):
        return render(request, "Accounts/signup.html")

    def post(self, request, format=None):
        serializer = UserResistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)

# Redirect to login page for browser-based requests
            redirect_response = handle_browser_redirect(request, 'login')
            if redirect_response:
                return redirect_response

            # Return API response for JSON requests
            return Response({'token': token, 'message': 'Registration Successful!!'}, status=status.HTTP_201_CREATED)

        # Handle validation errors
        return handle_form_response(request, "Accounts/signup.html", serializer.errors)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request):
        return render(request, "Accounts/login.html")

    def post(self, request, format=None):
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)

                # Redirect to dashboard for browser-based requests
                redirect_response = handle_browser_redirect(request, 'HomePage')
                if redirect_response:
                    return redirect_response

                # Return API response for JSON requests
                return Response({'token': token, 'message': 'Login Successful!!'}, status=status.HTTP_200_OK)

            # Invalid credentials
            return handle_form_response(request, "Accounts/login.html", {
                "non_field_errors": ["Email or password is not valid"]
            })

        # Handle serializer errors
        return handle_form_response(request, "Accounts/login.html", serializer.errors)


class ProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializers(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotUserPasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ForgotUserPasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password change successful!!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password reset email sent, please check your email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordRestview(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, token, uid, format=None):
        serializer = UserPasswordRestSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password reset successful!!!.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def Home(request):
    return render(request, "Accounts/home.html")
