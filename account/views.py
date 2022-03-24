from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserChangePasswordSerializer, UserLoginSerializer, UserProfileSerializer, UserSerializer, UserSetResetPasswordSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# create token manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistrations(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # after save registration get token 
            token = get_tokens_for_user(user)   

            return Response({'token': token,'msg': 'registration successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Userlogin(APIView):
    def post(self, request, formate=None):
        serializer = UserLoginSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email=email, password = password)
            token = get_tokens_for_user(user)   

            if user is not None:
                return Response({'token': token, 'msg': 'login success'}, status=status.HTTP_200_OK)
            
            else:
                return Response({'errors': {'non_field_errors':['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class UserProfileview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, formate=None):
        serializer = UserChangePasswordSerializer(data = request.data, context={'user': request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'change password successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

        
class UserSetResetPassword(APIView):
    def post(self, request, format=None):
        serializer = UserSetResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'password reset lint send, please check your email !'}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors)







