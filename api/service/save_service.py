import os
import shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from api.model.error import IncorrectFileType


def save_file(file) -> None:
    file_type = _get_file_type(file.name)
    if file_type not in settings.ALLOWED_MEDIA_TYPE:
        raise IncorrectFileType
    fs = FileSystemStorage()
    file_name = f'all_data.{file_type}'
    _remove_exists(fs, file_name)
    fs.save(file_name, file)


def create_excel_doc(template_name: str, workload_name: str) -> None:
    shutil.copy(template_name, workload_name)


def _get_file_type(file_name: str) -> str:
    return file_name.split('.')[-1]


def _remove_exists(fs: FileSystemStorage, file_name: str) -> None:
    if fs.exists(file_name):
        os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
