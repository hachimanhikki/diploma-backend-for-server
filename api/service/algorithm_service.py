from api.model.models import GroupSubject, Subject
from api.service.db_service import populate_workload, update_teacher_total_hours


def calculate_workload():
    subjects = Subject.objects.all()
    # for subject in subjects:
    #     _calculate_hours(subject)
    _calculate_hours(subjects[6])
    # print([(i, subjects[i]) for i in range(len(subjects))])


def _calculate_hours(subject: Subject) -> None:
    groups = GroupSubject.objects.filter(subject__exact=subject)
    groups_count = len(groups)
    teachers = subject.teachers.all()
    teachers_count = len(teachers)
    lecture_count = subject.lecture_count
    if not teachers:
        return

    # Average hour to one teacher
    # remainder goes to the last teacher
    one_teacher_hour = ((subject.total_hour // teachers_count) // 10) * 10
    remainder = subject.total_hour - teachers_count * one_teacher_hour
    one_teacher_groups = groups_count // teachers_count

    # remain_hours is remaining hours to distribute
    # hours is total hour assigning to the teacher
    # teacher_groups is average number of groups to one teacher
    remain_hours = [one_teacher_hour] * teachers_count
    remain_hours[-1] += remainder
    hours = remain_hours.copy()
    # prac_teacher_groups = [one_teacher_groups] * teachers_count

    # lec_teacher_groups, prac_teacher_groups не правильно используются
    # one_teacher_groups нужно заменить prac_teacher_groups,
    # потому что количестов групп может быть не кратным количеству учителей

    prac_teacher_groups = _distribute_prac_teachers(
        groups_count, teachers_count)
    lec_teacher_groups = _distribute_lecture_teachers(
        groups_count, lecture_count, teachers_count)

    # Compute lecture hours, lab hours, office hours, practice hours
    _calculate_all_hours(remain_hours, subject, one_teacher_groups)

    # practice_count is remaining practice lessons to distibure
    practice_count = subject.practice_count - \
        (one_teacher_groups * teachers_count)

    # Distrubute remaining practice lessons
    _calculate_remaining_hours(remain_hours, hours, subject,
                               prac_teacher_groups, practice_count)

    update_teacher_total_hours(teachers, hours)
    populate_workload(teachers, prac_teacher_groups,
                      lec_teacher_groups, groups)


def _distribute_prac_teachers(groups_count: int, teachers_count: int) -> list:
    return _distribute_groups_teachers(groups_count, teachers_count)


def _distribute_lecture_teachers(groups_count: int, lecture_count: int, teachers_count: int) -> list:
    return _distribute_groups_teachers(groups_count, lecture_count, teachers_count)


def _distribute_groups_teachers(count_1: int, count_2: int, count_3: int = 0) -> list:
    base, extra = divmod(count_1, count_2)
    result = [base + (i < extra) for i in range(count_2)]
    if len(result) < count_3:
        result.extend([0] * (count_3 - count_2))
    return result


def _calculate_all_hours(remain_hours: list, subject: Subject, one_teacher_groups: int) -> None:
    subject_lecture_count = subject.lecture_count
    subject_lab_count = subject.lab_count
    for i in range(len(remain_hours)):
        if subject_lecture_count > 0:
            remain_hours[i] -= subject.lecture_hour
            subject_lecture_count -= 1
        if subject_lab_count > 0:
            remain_hours[i] -= subject.lab_hour
            subject_lab_count -= 1
        remain_hours[i] -= subject.office_hour
        remain_hours[i] -= subject.practice_hour * one_teacher_groups


def _calculate_remaining_hours(remain_hours: list, hours: list, subject: Subject, teacher_groups: list, practice_count: int) -> None:
    for i in range(1, len(remain_hours)):
        remain_hours[i] += remain_hours[i - 1]
        hours[i] += remain_hours[i - 1]
        hours[i - 1] -= remain_hours[i - 1]
        remain_hours[i - 1] = 0
        while remain_hours[i] >= subject.practice_hour and practice_count > 0:
            remain_hours[i] -= subject.practice_hour
            practice_count -= 1
            teacher_groups[i] += 1
