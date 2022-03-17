from api.service.excel_parser_service import parse_teachers, parse_subjects, parse_subjects_for_teacher
from config.settings import DepartmentEnum
from api.model.models import Department, Subject, Teacher


def populate_database() -> None:
    if not Department.objects.exists():
        _populate_departments()
    if Teacher.objects.exists():
        Teacher.objects.all().delete()
    _populate_teachers()
    if Subject.objects.exists():
        Subject.objects.all().delete()
    _populate_subjects(3)
    _connect_subject_teacher()


def _populate_departments() -> None:
    for d in DepartmentEnum:
        department = Department(id=d.get_id(), name=d.value)
        department.save()


def _populate_teachers() -> None:
    teachers = parse_teachers()
    for teacher in teachers:
        teacher.one_rate = 560
        teacher.load = 1.0
        teacher.department_id = DepartmentEnum.computer_engineering.get_id()
        teacher.save()


def _populate_subjects(course_number: int) -> None:
    subjects = parse_subjects(course_number)
    for subject in subjects:
        subject.save()


def _connect_subject_teacher() -> None:
    teachers = Teacher.objects.all()
    for teacher in teachers:
        subject_names = parse_subjects_for_teacher(teacher)
        subjects = Subject.objects.filter(name__in=subject_names)
        teacher.subjects.add(*subjects)
