from . import views
from django.urls import path, include

urlpatterns = [
    path('check', views.check),
    path('flows/', include('flows.urls')),
    path('load/', include('load.urls')),
    path('', include('accounts.urls')),
    path('workload_save', include('workload.urls')),
]
