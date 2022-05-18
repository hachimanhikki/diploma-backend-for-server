from django.conf import settings
from django.http import JsonResponse
from api.model.models import Workload
from api.service.algorithm_service import calculate_workload
from api.service.db_service import populate_database
from api.service.excel_create_service import create_excel_workload
from accounts.models import Teacher


def check(request):
    populate_database()
    # Workload.objects.all().delete()
    # Teacher.objects.all().update(total_hour=0)
    # calculate_workload()
    # create_excel_workload()
    return JsonResponse({'success': True})
