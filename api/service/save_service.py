import os
import shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from api.model.error import IncorrectFileType


def save_file(file, is_flows: bool = False) -> None:
    file_type = _get_file_type(file.name)
    if file_type not in settings.ALLOWED_MEDIA_TYPE:
        raise IncorrectFileType
    fs = FileSystemStorage()
    if is_flows:
        file_name = f'all_data.{file_type}'
    else:
        file_name = f'schedule.{file_type}'
    _remove_exists(fs, file_name)
    fs.save(file_name, file)


def create_excel_doc(template_path: str, workload_path: str) -> None:
    shutil.copy(template_path, workload_path)


def _get_file_type(file_name: str) -> str:
    return file_name.split('.')[-1]


def _remove_exists(fs: FileSystemStorage, file_name: str) -> None:
    if fs.exists(file_name):
        os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
