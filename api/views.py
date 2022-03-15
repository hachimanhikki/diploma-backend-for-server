from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .api_services import save_file


@csrf_exempt
def upload(request):
    if request.method == "POST":
        try:
            save_file(request.FILES[settings.UPLOADED_FILE_NAME])
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': e.message})
    return JsonResponse({'success': False, 'message': 'File is not uploaded'})
