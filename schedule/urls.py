from . import views
from django.urls import path

urlpatterns = [
    path('upload', views.upload),
    path('file_name', views.file_name),
    path('download', views.download),
    path('groups', views.schedule_groups),
    path('teachers', views.schedule_teachers),
    path('by_group', views.schedule_by_group),
    path('by_teacher', views.schedule_by_teacher)
]
