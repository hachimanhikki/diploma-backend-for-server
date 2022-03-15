from config.settings import DepartmentEnum
from ..model.models import Department, Teacher


def populate_database() -> None:
    if not Department.objects.exists():
        _set_departments()
    if Teacher.objects.exists():
        Teacher.objects.all().delete()


def _set_departments() -> None:
    for d in DepartmentEnum:
        department = Department(id=d.get_id(), name=d.value)
        department.save()
