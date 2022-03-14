import os
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage


def save_file(file) -> JsonResponse:
    file_type = _get_file_type(file.name)
    if file_type not in settings.ALLOWED_MEDIA_TYPE:
        return JsonResponse({'success': False, 'message': 'Incorrect file type'})
    fs = FileSystemStorage()
    file_name = f'Формирование потоков.{file_type}'
    _remove_exists(fs, file_name)
    fs.save(file_name, file)
    return JsonResponse({'success': True})


def _get_file_type(file_name: str) -> str:
    return file_name.split('.')[-1]


def _remove_exists(fs: FileSystemStorage, file_name: str) -> None:
    if fs.exists(file_name):
        os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
