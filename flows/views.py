import os
from django.conf import settings
from django.http import HttpResponse
from api.model.serializers import GroupSerializer
from accounts.serializers import TeacherGETSerializer
from api.service.db_service import groups_statistic, populate_database, teacher_statistic
from api.service.save_service import save_file, is_file_exists
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.model.static_models import HTTPMethod
from api.model.error import IncorrectFileType, FileDoesntExists
import openpyxl


@api_view([HTTPMethod.post])
@permission_classes([IsAuthenticated])
def upload(request):
    try:
        save_file(request.FILES[settings.FLOWS_FILE_NAME], True)
        populate_database()
        return Response({'success': True})
    except IncorrectFileType as e:
        return Response({'message': e.message}, status=e.status)
    except Exception as e:
        return Response({'message': "Error"}, status=400)


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def file_name(request):
    file_name = 'all_data.xlsx'
    if not is_file_exists(file_name):
        return Response({'message': FileDoesntExists.message}, status=FileDoesntExists.status)
    return Response({'file_name': file_name})


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def download(request):
    file_name = 'all_data.xlsx'
    if not is_file_exists(file_name):
        return Response({'message': FileDoesntExists.message}, status=FileDoesntExists.status)
    wb = openpyxl.load_workbook(os.path.join(settings.MEDIA_ROOT, file_name))
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    wb.save(response)
    return response


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def course_statistics(request):
    response = {}
    groups_stat = groups_statistic()
    for course, groups in groups_stat.items():
        total_number_of_students = sum(
            groups.values_list('number_of_students', flat=True))
        serializer = GroupSerializer(groups, many=True)
        response[course] = {
            "total_number_of_students": total_number_of_students,
            "groups": serializer.data
        }
    return Response(response)


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def teacher_statistics(request):
    response = {}
    teacher_stat = teacher_statistic()
    for kpi, teachers in teacher_stat.items():
        total_count = len(teachers)
        serializer = TeacherGETSerializer(teachers)
        response[kpi] = {
            "total_count": total_count,
            "teachers": serializer.data
        }
    return Response(response)
