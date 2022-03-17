from api.service.excel_parser_service import fetch_teachers
from config.settings import DepartmentEnum
from api.model.models import Department, Teacher


def populate_database() -> None:
    if not Department.objects.exists():
        _populate_departments()
    if Teacher.objects.exists():
        Teacher.objects.all().delete()
    _populate_teachers()


def _populate_departments() -> None:
    for d in DepartmentEnum:
        department = Department(id=d.get_id(), name=d.value)
        department.save()


def _populate_teachers() -> None:
    teachers = fetch_teachers()
    for teacher in teachers:
        teacher.one_rate = 560
        teacher.load = 1.0
        teacher.department_id = DepartmentEnum.computer_engineering.get_id()
        teacher.save()
