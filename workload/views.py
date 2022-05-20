from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.model.serializers import WorkloadSerializer
from api.model.static_models import HTTPMethod


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
