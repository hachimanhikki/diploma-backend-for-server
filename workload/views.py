from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.model.static_models import HTTPMethod
from api.model.serializers import GroupSubjectSerializer, WorkloadSerializer


@api_view([HTTPMethod.get])
def available_by_subject(request):
    serializer = GroupSubjectSerializer(by_subject=True, available=True)
    return Response(serializer.data)


@api_view([HTTPMethod.get])
def available_by_group(request):
    serializer = GroupSubjectSerializer(by_group=True, available=True)
    return Response(serializer.data)


@api_view([HTTPMethod.post])
def workload_save(request):
    if request.method == HTTPMethod.post:
        serializer = WorkloadSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = True
        else:
            data = serializer.errors
        return Response(data)


@api_view([HTTPMethod.get])
def workload_get(request):
    serializer = WorkloadSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['success'] = True
    else:
        data = serializer.errors
    return Response(data)
