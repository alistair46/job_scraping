# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserResistrationSerializer ,UserLoginSerializers ,ProfileSerializers ,ForgotUserPasswordSerializer ,SendPasswordResetEmailSerializer,UserPasswordRestSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from Accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


#To generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserResistrationView(APIView):
    renderer_classes=[UserRenderer] # for frontend to show error
    def post(self,request,format=None):
        serializer=UserResistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
# generate token after user is saved 
            token=get_tokens_for_user(user)  
# sending token as response          
            return Response({'token':token,'message':'Registration Sucessfull !!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes=[UserRenderer] # for frontend to show error
    def post(self,request,format=None):
        serializer=UserLoginSerializers(data=request.data)
# Here we are authenitcate user using django authenticate method  where we pass email and password to get verified
        if (serializer.is_valid(raise_exception=True)):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'message':'login Sucessfull !!'}, status=status.HTTP_200_OK)
            else:
               return Response({'errors':{'non_field_errors':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer= ProfileSerializers(request.user)
        #if serializer.is_valid():
            #return Response (serializer.data,status=status.HTTP_200_OK)
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
    


'''from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def Home(request):
    return render(request, "Accounts/home.html")
    


def Signup(request):
    return render(request, "Accounts/signup.html")

def login(request):
    return render(request, "Accounts/login.html")
'''