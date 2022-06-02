from .views import registration_view, CustomAuthToken, verify_email
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register', registration_view, name='register'),
    path('login', CustomAuthToken.as_view(), name='login'),
    path('verify-email', verify_email, name='verify-email'),
]
