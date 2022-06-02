from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from api.model.static_models import HTTPMethod
from accounts.serializers import TeacherSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from config import settings
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import random

def generate_code():
    number_list = [x for x in range(10)]
    code_items = []
    for i in range(5):
        num = random.choice(number_list)
        code_items.append(num)
        code_str = ''.join(str(item) for item in code_items)
    return code_str


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'first_name': user.first_name,
            'second_name': user.second_name,
            'kpi': user.kpi,
            'username': user.username,
            'token': token.key,
            'email': user.email,
            'is_head': user.is_admin,
            'department_name': user.department.name
        })


@api_view([HTTPMethod.post])
def verify_email(request):
    if request.method == HTTPMethod.post:
        data = request.data.dict()
        print(data)
        code = generate_code()
        teacher_email = data['email']
        teacher_name = data['first_name']
        email_body = 'Greetings, ' + teacher_name + '. Use this code below to verify your email \n' + code
        email_data = {'email_body' : email_body, 'email_subject' : 'Verify your email', 'email_to': teacher_email}
        
        Util.send_email(email_data)
        data['code'] = code
        return Response(data)


@api_view([HTTPMethod.post])
def registration_view(request):
    if request.method == HTTPMethod.post:
        serializer = TeacherSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            teacher = serializer.save()
            data['first_name'] = teacher.first_name
            data['second_name'] = teacher.second_name
            data['kpi'] = teacher.kpi
            data['username'] = teacher.username
            data['email'] = teacher.email
            data['code'] = code
            data['token'] = token
            data['is_head'] = teacher.is_admin
            data['department_name'] = teacher.department.name
        else:
            data = serializer.errors
        return Response(data)
    
