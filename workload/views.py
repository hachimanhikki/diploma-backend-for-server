from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from workload.serializers import WorkloadSerializer

@api_view(['POST',])
def workload_save(request):

    if request.method == 'POST':
        serializer = WorkloadSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'success'
        else:
            data = serializer.errors
        return Response(data)