from .views import registration_view
from django.urls import path


urlpatterns = [
    path('register/', registration_view, name='register'),
]
