from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.model.models import Teacher, Workload
from api.service.algorithm_service import calculate_workload
from api.service.db_service import populate_database
from api.service.excel_create_service import create_excel_workload
from .service.save_service import save_file


@csrf_exempt
def upload(request):
    if request.method == "POST":
        try:
            save_file(request.FILES[settings.UPLOADED_FILE_NAME])
            populate_database()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e.message})
    return JsonResponse({'success': False, 'message': 'File is not uploaded'})


def check(request):
    # populate_database()
    Workload.objects.all().delete()
    Teacher.objects.all().update(total_hour=0)
    calculate_workload()
    create_excel_workload()
    return JsonResponse({'success': True})
