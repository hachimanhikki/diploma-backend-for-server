from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.service.db_service import populate_database
from api.service.save_service import save_file
from rest_framework.decorators import api_view
from api.model.static_models import HTTPMethod


@csrf_exempt
@api_view([HTTPMethod.post])
def upload(request):
    if request.method == "POST":
        try:
            save_file(request.FILES[settings.UPLOADED_FILE_NAME])
            populate_database()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e.message}, status=e.status)
    return JsonResponse({'success': False, 'message': 'File is not uploaded'}, status=500)
