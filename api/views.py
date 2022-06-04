from django.conf import settings
from api.model.models import Subject, Workload
from api.service.algorithm_service import calculate_workload
from api.service.db_service import populate_database, populate_schedule
from api.service.excel_create_service import create_excel_workload
from accounts.models import Teacher
from rest_framework.response import Response
from api.model.static_models import HTTPMethod
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.service.excel_parser_service import parse_groups, parse_subjects


@api_view([HTTPMethod.get])
# @permission_classes([IsAuthenticated])
# Authorization: Token <token>
def check(request):
    # populate_database()
    # Workload.objects.all().delete()
    # Teacher.objects.all().update(total_hour=0)
    # calculate_workload()
    # create_excel_workload()
    # populate_schedule()
    # create_excel_workload()
    # Teacher.objects.get(id=7).delete()
    # populate_database()
    # parse_groups()
    return Response({'success': 12})
