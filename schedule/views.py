import os
from django.conf import settings
from django.http import HttpResponse
import openpyxl
from api.model.serializers import ScheduleSerializer
from api.service.db_service import populate_schedule
from api.service.save_service import is_file_exists, save_file
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.model.static_models import HTTPMethod
from api.model.error import IncorrectFileType, FileDoesntExists


@api_view([HTTPMethod.post])
@permission_classes([IsAuthenticated])
def upload(request):
    if request.method == HTTPMethod.post:
        try:
            save_file(request.FILES[settings.SCHEDULE_FILE_NAME])
            populate_schedule()
            return Response({'success': True})
        except IncorrectFileType as e:
            return Response({'message': e.message}, status=e.status)
        except Exception as e:
            return Response({'message': "Error"}, status=400)
    return Response({'message': 'File is not uploaded'}, status=500)


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def file_name(request):
    file_name = 'schedule.xlsx'
    if not is_file_exists(file_name):
        return Response({'message': FileDoesntExists.message}, status=FileDoesntExists.status)
    return Response({'file_name': file_name})


@api_view([HTTPMethod.get])
@permission_classes([IsAuthenticated])
def download(request):
    file_name = 'schedule.xlsx'
    if not is_file_exists(file_name):
        return Response({'message': FileDoesntExists.message}, status=FileDoesntExists.status)
    wb = openpyxl.load_workbook(os.path.join(settings.MEDIA_ROOT, file_name))
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    wb.save(response)
    return response


@api_view([HTTPMethod.get])
def schedule_groups(request):
    serializer = ScheduleSerializer()
    groups = serializer.get_groups()
    return Response(groups)


@api_view([HTTPMethod.get])
def schedule_teachers(request):
    serializer = ScheduleSerializer()
    teachers = serializer.get_teachers()
    return Response(teachers)


@api_view([HTTPMethod.get])
def schedule_by_group(request):
    serializer = ScheduleSerializer(
        group_name=request.query_params['group_name'], by_group=True)
    return Response(serializer.data)


@api_view([HTTPMethod.get])
def schedule_by_teacher(request):
    serializer = ScheduleSerializer(
        teacher_name=request.query_params['teacher_name'], by_teacher=True)
    return Response(serializer.data)
