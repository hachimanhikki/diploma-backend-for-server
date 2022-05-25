from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.model.static_models import HTTPMethod
from api.model.serializers import GroupSubjectSerializer, WorkloadSerializer, WorkloadGETSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
    serializer = WorkloadGETSerializer(teacher_name=request.data['teacher_username'], by_teacher=True)
    return Response(serializer.data)
