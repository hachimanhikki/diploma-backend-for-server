from api.model.models import Department, Group, GroupSubject, Subject


def department_to_dict(department: Department) -> dict:
    res = {
        'name': department.name,
    }
    return res


def subject_to_dict(subject: Subject) -> dict:
    res = {
        'name': subject.name.capitalize(),
        'credits': subject.credits,
        'lecture_count': subject.lecture_count,
        'practice_count': subject.practice_count,
        'office_count': subject.office_count,
        'lab_count': subject.lab_count,
        'lecture_hour': subject.lecture_hour,
        'practice_hour': subject.practice_hour,
        'office_hour': subject.office_hour,
        'lab_hour': subject.lab_hour,
        'total_hour': subject.total_hour,
        'department': department_to_dict(subject.department),
    }
    return res


def group_to_dict(group: Group) -> dict:
    res = {
        'name': group.name,
        'code': group.code,
        'course': group.course,
        'number_of_students': group.number_of_students,
    }
    return res


def group_subject_to_dict(group_subject: GroupSubject) -> dict:
    res = {
        'subject': subject_to_dict(group_subject.subject),
        'group': group_to_dict(group_subject.group),
        'trimester': group_subject.trimester,
    }
    return res


def groups_subjects_to_dict(groups_subjects: list, by_subject: bool = False, by_group: bool = False) -> dict:
    res = {}

    if by_subject:
        res = {
            'subject': subject_to_dict(groups_subjects[0].subject),
            'groups': [group_to_dict(group_subject.group) for group_subject in groups_subjects],
            'trimester': groups_subjects[0].trimester,
        }
    elif by_group:
        res = {
            'group': group_to_dict(groups_subjects[0].group),
            'subjects': [subject_to_dict(group_subject.subject) for group_subject in groups_subjects],
            'trimester': groups_subjects[0].trimester,
        }

    return res
