import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage


def hello(request):
    return JsonResponse({'message': 'hello'})


@csrf_exempt
def upload(request):
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        uploaded_file_type = uploaded_file.name.split('.')[-1]
        if uploaded_file_type not in ['xlsx', 'xls']:
            return JsonResponse({'message': 'Incorrect file type'})
        fs = FileSystemStorage()
        file_name = f'Формирование потоков.{uploaded_file_type}'
        if fs.exists(file_name):
            os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
        fs.save(file_name, uploaded_file)
        return JsonResponse({'message': 'File is uploaded'})
    return JsonResponse({'message': 'File is not uploaded'})
