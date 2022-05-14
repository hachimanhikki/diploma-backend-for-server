from django.http import JsonResponse
from api.model.models import GroupSubject
from api.service.model_to_dict_service import group_subject_to_dict, groups_subjects_to_dict


def available(request):
    response = []
    groups_subjects = GroupSubject.objects.all()
    for group_subject in groups_subjects:
        response.append(group_subject_to_dict(group_subject))
    return JsonResponse(response, safe=False)


def available_by_subject(request):
    response = []
    subjects = set(GroupSubject.objects.values_list(
        'subject', flat=True).distinct())
    for subject_id in subjects:
        groups_subjects = GroupSubject.objects.filter(
            subject_id__exact=subject_id).order_by('group__name')
        response.append(groups_subjects_to_dict(
            groups_subjects, by_subject=True))
    return JsonResponse(response, safe=False)


def available_by_group(request):
    response = []
    groups = set(GroupSubject.objects.values_list(
        'group', flat=True).distinct())
    for group_name in groups:
        groups_subjects = GroupSubject.objects.filter(
            group__name__exact=group_name).order_by('group__name')
        response.append(groups_subjects_to_dict(
            groups_subjects, by_group=True))
    return JsonResponse(response, safe=False)
