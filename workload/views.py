from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.model.static_models import HTTPMethod
from api.model.serializers import GroupSubjectSerializer, WorkloadSerializer, WorkloadGETSerializer, refresh_teacher_and_subject
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.service.excel_create_service import create_excel_workload_for_teacher, create_excel_workload
from accounts.models import Teacher
from api.model.models import Subject, Workload


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def available_by_subject(request):
    serializer = GroupSubjectSerializer(by_subject=True, available=True)
    return Response(serializer.data)


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def available_by_group(request):
    serializer = GroupSubjectSerializer(by_group=True, available=True)
    return Response(serializer.data)


@api_view([HTTPMethod.post])
@permission_classes([IsAuthenticated])
def workload_save(request):
    if request.method == HTTPMethod.post:
        serializer = WorkloadSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save_data()
            data['success'] = True
        else:
            data = serializer.errors
        return Response(data)

@api_view([HTTPMethod.post])
@permission_classes([IsAuthenticated])
def workload_edit(request):
    if request.method == HTTPMethod.post:
        serializer = WorkloadSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.edit_data()
            data['success'] = True
        else:
            data = serializer.errors
        return Response(data)

@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def workload_get(request):
    serializer = WorkloadGETSerializer(
        teacher_name=request.query_params['teacher_username'], by_teacher=True)
    return Response(serializer.data)


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def workload_get_all(request):
    serializer = WorkloadGETSerializer(all=True)
    return Response(serializer.data)


@api_view([HTTPMethod.post])
@permission_classes([IsAuthenticated])
def workload_delete(request):
    username = request.data['teacher_username']
    subject_name = request.data['subject_name']
    teacher = Teacher.objects.get(username__exact=username)
    subject = Subject.objects.get(name__exact=subject_name)
    teacher, subject = refresh_teacher_and_subject(teacher, subject, refresh=True)
    subject.teachers.remove(teacher)
    teacher.save()
    subject.save()
    Workload.objects.filter(group_subject__subject__exact=subject, teacher__exact=teacher).delete()
    return Response({"success": True})


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def download(request):
    file_name = 'Нагрузка.xlsx'
    wb = create_excel_workload_for_teacher(
        request.query_params['teacher_username'])
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    wb.save(response)
    return response


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def download_all(request):
    file_name = 'Нагрузка.xlsx'
    wb = create_excel_workload()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    wb.save(response)
    return response
