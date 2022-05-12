from . import views
from django.urls import path, include

urlpatterns = [
    path('check', views.check),
    path('flows/', include('flows.urls'))
]
