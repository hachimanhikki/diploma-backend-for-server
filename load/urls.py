from . import views
from django.urls import path

urlpatterns = [
    path('available/by_subject', views.available_by_subject),
    path('available/by_group', views.available_by_group),
]
