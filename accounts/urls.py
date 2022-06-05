from .views import change_kpi, change_load, change_password, registration_view, CustomAuthToken, verify_email
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register', registration_view, name='register'),
    path('login', CustomAuthToken.as_view(), name='login'),
    path('verify-email', verify_email, name='verify-email'),
    path('change_kpi', change_kpi, name='change_kpi'),
    path('change_load', change_load, name='change_load'),
    path('change_password', change_password, name='change_password'),
]
