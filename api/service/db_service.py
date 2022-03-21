from tokenize import group
from api.service.excel_parser_service import parse_groups, parse_groups_for_subject, parse_teachers, parse_subjects, parse_subjects_for_teacher
from config.settings import DepartmentEnum
from api.model.models import Department, Group, Subject, Teacher


def populate_database() -> None:
    if not Department.objects.exists():
        _populate_departments()
    _delete_all_existing()
    _populate_groups()
    _populate_teachers()
    _populate_subjects(3)
    _connect_subject_teacher()
    _connect_group_subject(3)


def _delete_all_existing() -> None:
    if Group.objects.exists():
        Group.objects.all().delete()
    if Teacher.objects.exists():
        Teacher.objects.all().delete()
    if Subject.objects.exists():
        Subject.objects.all().delete()


def _populate_departments() -> None:
    for d in DepartmentEnum:
        department = Department(id=d.id, name=d.value)
        department.save()


def _populate_teachers() -> None:
    teachers = parse_teachers()
    for teacher in teachers:
        teacher.one_rate = 560
        teacher.load = 1.0
        teacher.department_id = DepartmentEnum.computer_engineering.id
        teacher.save()


def _populate_subjects(course: int) -> None:
    subjects = parse_subjects(course)
    for subject in subjects:
        subject.save()


def _populate_groups() -> None:
    groups = parse_groups()
    for group in groups:
        group.save()


def _connect_subject_teacher() -> None:
    teachers = Teacher.objects.all()
    for teacher in teachers:
        subject_names = parse_subjects_for_teacher(teacher)
        subjects = Subject.objects.filter(name__in=subject_names)
        teacher.subjects.add(*subjects)


def _connect_group_subject(course: int) -> None:
    subjects = Subject.objects.all()
    allowed_group_codes = Group.objects.filter(
        course__exact=course).values_list('code', flat=True).distinct()
    for subject in subjects:
        groups_list = parse_groups_for_subject(
            course, subject, allowed_group_codes)
        for group_code, trimester in groups_list:
            groups = Group.objects.filter(
                course__exact=course, code__exact=group_code)
            subject.groups.add(
                *groups, through_defaults={'trimester': trimester})
            subject.save()
