from . import views
from django.urls import path, include

urlpatterns = [
    path('check', views.check),
    path('flows/', include('flows.urls')),
    path('', include('accounts.urls')),
    path('workload/', include('workload.urls')),
    path('schedule/', include('schedule.urls'))
]
