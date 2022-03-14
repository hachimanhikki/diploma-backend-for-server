import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .api_services import save_file


def hello(request):
    return JsonResponse({'message': 'hello'})


@csrf_exempt
def upload(request):
    if request.method == "POST":
        return save_file(request.FILES[settings.UPLOADED_FILE_NAME])
    return JsonResponse({'success': False, 'message': 'File is not uploaded'})
