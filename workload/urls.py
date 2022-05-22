from .views import workload_save, workload_get
from django.urls import path

urlpatterns = [
    path('save', workload_save, name='save'),
    path('get', workload_get, name='get'),
]
