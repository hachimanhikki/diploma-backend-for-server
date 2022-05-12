from api.model.models import GroupSubject, Subject
from api.service.db_service import populate_workload, update_teacher_total_hours


def calculate_workload():
    subjects = Subject.objects.all()
    for subject in subjects:
        _calculate_hours(subject)


def _calculate_hours(subject: Subject) -> None:
    groups = GroupSubject.objects.filter(subject__exact=subject)
    groups_count = len(groups)
    teachers = subject.teachers.all()
    teachers_count = len(teachers)
    lecture_count = subject.lecture_count
    if not teachers:
        return

    # prac_teacher_groups is practice lessons count
    # lec_teacher_groups is lecture lessons count
    prac_teacher_groups = _distribute_prac_teachers(
        groups_count, teachers_count)
    lec_teacher_groups = _distribute_lecture_teachers(
        groups_count, lecture_count, teachers_count)

    # Compute lecture hours, lab hours, office hours, practice hours
    total_hours = [0] * teachers_count
    _calculate_all_hours(total_hours, subject, prac_teacher_groups)

    update_teacher_total_hours(teachers, total_hours)
    populate_workload(teachers, prac_teacher_groups,
                      lec_teacher_groups, groups)


def _distribute_prac_teachers(groups_count: int, teachers_count: int) -> list:
    return _distribute_groups_teachers(groups_count, teachers_count)[::-1]


def _distribute_lecture_teachers(groups_count: int, lecture_count: int, teachers_count: int) -> list:
    return _distribute_groups_teachers(groups_count, lecture_count, teachers_count)


def _distribute_groups_teachers(count_1: int, count_2: int, count_3: int = 0) -> list:
    base, extra = divmod(count_1, count_2)
    result = [base + (i < extra) for i in range(count_2)]
    if len(result) < count_3:
        result.extend([0] * (count_3 - count_2))
    return result


def _calculate_all_hours(total_hours: list, subject: Subject, prac_teacher_groups: list) -> None:
    subject_lecture_count = subject.lecture_count
    subject_lab_count = subject.lab_count
    for i in range(len(total_hours)):
        if subject_lecture_count > 0:
            total_hours[i] += subject.lecture_hour
            subject_lecture_count -= 1
        if subject_lab_count > 0:
            total_hours[i] += subject.lab_hour
            subject_lab_count -= 1
        total_hours[i] += subject.office_hour
        total_hours[i] += subject.practice_hour * prac_teacher_groups[i]
