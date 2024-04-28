from django.contrib import admin
from django.urls import path
from accounts.views import UserRegistration, UserLogin, ProfileView, UserChangePasswordView, SendPasswordResetEmailView,UserPasswordResetView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profileview'),
    path('changepass/',
         UserChangePasswordView.as_view(),
         name='userchangepassword'),
    path('send-reset-passwordemail/',
         SendPasswordResetEmailView.as_view(),
         name='send-reset-password-email'),
   path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]
