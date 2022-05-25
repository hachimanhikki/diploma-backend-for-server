from . import views
from django.urls import path


urlpatterns = [
    path('save', views.workload_save),
    path('edit', views.workload_edit),
    path('get', views.workload_get),
    path('delete_by_subject', views.workload_delete),
    path('all/get', views.workload_get_all),
    path('available/by_subject', views.available_by_subject),
    path('available/by_group', views.available_by_group),
    path('download', views.download),
    path('all/download', views.download_all),
]
