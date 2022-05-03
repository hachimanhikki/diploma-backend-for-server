from api.service.excel_parser_service import parse_groups, parse_groups_for_subject, parse_teachers, parse_subjects, parse_subjects_for_teacher
from config.settings import DepartmentEnum
from api.model.models import Department, Group, Subject, Teacher, Workload


courses = [2, 3]


def populate_database() -> None:
    if not Department.objects.exists():
        _populate_departments()
    _delete_all_existing()
    _populate_groups()
    _populate_teachers()
    _populate_all_courses()
    _connect_subject_teacher()
    _connect_all_group_subject()


def update_teacher_total_hours(teachers: list, hours: list) -> None:
    for i in range(len(teachers)):
        teachers[i].total_hour += hours[i]
        teachers[i].save()


def populate_workload(teachers: list, prac_teacher_groups: list, lec_teacher_groups: list, groups: list) -> None:
    prac_range = [0, prac_teacher_groups[0]]
    lec_range = [0, lec_teacher_groups[0]]
    for i in range(len(teachers)):
        bottom = min(prac_range[0], lec_range[0])
        top = max(prac_range[1], lec_range[1])
        if (lec_teacher_groups[i] == 0):
            bottom = prac_range[0]
            top = prac_range[1]
        for j in range(bottom, top):
            workload = Workload()
            workload.teacher = teachers[i]
            workload.is_lecture = lec_range[0] <= j <= lec_range[1] - 1
            workload.is_practice = prac_range[0] <= j <= prac_range[1] - 1
            workload.is_lab = False
            workload.group_subject = groups[j]
            workload.save()
        if i + 1 < len(teachers):
            prac_range[0] += prac_teacher_groups[i]
            prac_range[1] += prac_teacher_groups[i + 1]
            lec_range[0] += lec_teacher_groups[i]
            lec_range[1] += lec_teacher_groups[i + 1]


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
        teacher.position = 'Преподаватель'
        teacher.kpi = 'Teacher'
        teacher.department_id = DepartmentEnum.computer_engineering.id
        teacher.save()


def _populate_all_courses():
    for course in courses:
        _populate_subjects(course)


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


def _connect_all_group_subject():
    for course in courses:
        _connect_group_subject(course)


def _connect_group_subject(course: int) -> None:
    subjects = Subject.objects.all()
    allowed_group_codes = set(Group.objects.filter(
        course__exact=course).values_list('code', flat=True).distinct())
    for subject in subjects:
        groups_list = parse_groups_for_subject(
            course, subject, allowed_group_codes)
        for group_code, trimester in groups_list:
            groups = Group.objects.filter(
                course__exact=course, code__exact=group_code)
            subject.groups.add(
                *groups, through_defaults={'trimester': trimester})
            subject.save()
