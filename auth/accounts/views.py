from django.shortcuts import render
from logging import raiseExceptions
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from accounts.renderers import UserRenderer
from accounts.serializers import (UserRegistrationSerializer, LoginSerializer,ProfileViewSerializer,
                                   UserPasswordResetSerializer, SendPasswordResetEmailSerializer,UserPasswordChangeSerializer)
from rest_framework_simplejwt.tokens import RefreshToken


#creating tokens manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# User RegistrationView
class UserRegistration(APIView):
  def post(self, request):
    serializer = UserRegistrationSerializer(data=request.data)
    # Validate method called
    if serializer.is_valid():
      # create method called from serializer
      user = serializer.save()
      token = get_tokens_for_user(user)
      return Response({"token": token, "msg": "Registration success"})
    return Response(serializer.errors, status=status.HTTP_201_CREATED)

# Login View
class UserLogin(APIView):
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get("email")
    password = serializer.data.get("password")
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({"token": token, "msg": "Login success"})
    else:
      return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

# View User Profile
class ProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request):
    serializer = ProfileViewSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Change password when password is already known
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request):
    serializer = UserPasswordChangeSerializer(data=request.data,context={'user': request.user})
    serializer.is_valid(raise_exception=True)
    return Response({"msg": "Password Changed successfully"})


# sending password reset link in the email
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg': 'Password reset link has been sent your to your email'}, status=status.HTTP_200_OK)


# Reset password
class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token):
    serializer = UserPasswordResetSerializer(data=request.data,context={'uid': uid,'token': token })
    serializer.is_valid(raise_exception=True)
    return Response({'msg': 'Password Reset Successfully'},status=status.HTTP_200_OK)
