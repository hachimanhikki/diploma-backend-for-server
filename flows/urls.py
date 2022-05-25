from . import views
from django.urls import path

urlpatterns = [
    path('upload', views.upload),
    path('file_name', views.file_name),
    path('download', views.download),
    path('course_statistics', views.course_statistics),
    path('teacher_statistics', views.teacher_statistics),
]
