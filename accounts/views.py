from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from accounts.serializers import TeacherSerializer


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = TeacherSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            teacher = serializer.save()
            data['response'] = 'succesfully registered a new user'
            data['email'] = teacher.email
            data['full_name'] = teacher.full_name
        else:
            data = serializer.errors
        return Response(data)