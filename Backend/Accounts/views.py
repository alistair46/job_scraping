from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (UserResistrationSerializer ,UserLoginSerializers ,
                          ProfileSerializers ,ForgotUserPasswordSerializer ,
                          SendPasswordResetEmailSerializer,UserPasswordRestSerializer, LogoutSerializer)
from rest_framework import status
from django.contrib.auth import authenticate,login
from Accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 
from django.core.exceptions import PermissionDenied

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
                login(request, user)  # This logs in the user
                token = get_tokens_for_user(user)
    # Store user's name in session
                request.session['user_name'] = user.Name  

                # Print the tokens in the terminal for debugging
                print("Access Token:", token['access'])
                print("Refresh Token:", token['refresh'])

                # Store the tokens in localStorage (to be used in frontend)
                response_data = {
                    'token': token,
                    'message': 'Login Successful!!',
                    'user': {
                        'id': user.id,
                        'Name': user.Name,
                        'email': user.email
                        }}
                # If content-type is not JSON, send the tokens back to frontend as well
                if request.headers.get('Content-Type') != 'application/json':
                    return redirect('HomePage')
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(
                {'errors': {'non_field_errors': ['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
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
    


@login_required(login_url='/api/login')  # Redirect to login page if not logged in       
def Home(request):
    user_name = request.session.get('user_name', 'User')  # Retrieve from session
    return render(request, "Accounts/home.html", {"username": user_name})


#!### Logout Class to logout user ####
#! logout thorugh post man shows logout sucessfull but in browser the user still seams logined 
#!  after clearing browser cookies the user seemes logout
class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Extract refresh_token from serializer data
                refresh_token = serializer.validated_data['refresh_token']
                
                # Blacklist the refresh token to invalidate it
                token = RefreshToken(refresh_token)
                token.blacklist()

                # Clear the session to log out the user
                request.session.flush()  # This will clear the session

                if request.headers.get('Content-Type') != 'application/json':
                    return redirect('login')

                # Respond back with success
                return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def Aboutus(request):
    return render(request, "Accounts/aboutus.html")
