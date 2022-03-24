from api.model.models import GroupSubject, Subject, Workload
from api.service.db_service import populate_workload, update_teacher_total_hours


def calculate_workload():
    subjects = Subject.objects.all()
    # for subject in subjects:
    #     _assign_hours(subject)
    #     print()
    print(subjects[0])
    _calculate_hours(subjects[0])


def distribute(groups, teachers):
    base, extra = divmod(groups, teachers)
    return [base + (i < extra) for i in range(teachers)]


def _calculate_hours(subject):
    groups = GroupSubject.objects.filter(subject__exact=subject)
    groups_count = len(groups)
    teachers = subject.teachers.all()

    if not teachers:
        return

    # Average hour to one teacher
    # remainder goes to the last teacher
    one_teacher_hour = ((subject.total_hour // len(teachers)) // 10) * 10
    remainder = subject.total_hour - len(teachers) * one_teacher_hour
    one_teacher_groups = groups_count // len(teachers)

    # remain_hours is remaining hours to distribute
    # hours is total hour assigning to the teacher
    # teacher_groups is average number of groups to one teacher
    remain_hours = [one_teacher_hour] * len(teachers)
    hours = [one_teacher_hour] * len(teachers)
    remain_hours[-1] += remainder
    hours[-1] += remainder
    prac_teacher_groups = [one_teacher_groups] * len(teachers)
    lec_teacher_groups = distribute(groups_count, lecture_count)
    if len(lec_teacher_groups) < len(teachers):
        lec_teacher_groups.extend([0] * (len(teachers) - lecture_count))
    # Compute lecture hours, lab hours, office hours, practice hours
    _calculate_all_hours(remain_hours, subject, one_teacher_groups)

    # practice_count is remaining practice lessons to distibure
    practice_count = subject.practice_count - \
        (one_teacher_groups * len(teachers))

    # Distrubute remaining practice lessons
    _calculate_remaining_hours(remain_hours, hours, subject,
                               prac_teacher_groups, practice_count)

    update_teacher_total_hours(teachers, hours)
    populate_workload(teachers, subject, prac_teacher_groups, lec_teacher_groups, groups)


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


def _assign_groups(teacher):
    pass
