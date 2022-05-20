from .views import workload_save
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', workload_save, name='workload_save'),
]
