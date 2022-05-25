from . import views
from django.urls import path

urlpatterns = [
    path('upload', views.upload),
    path('file_name', views.file_name),
    path('download', views.download)
]
