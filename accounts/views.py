from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from api.model.static_models import HTTPMethod
from accounts.serializers import TeacherSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from .utils import Util
import random


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
            'position': user.position,
            'one_rate': user.one_rate,
            'username': user.username,
            'token': token.key,
            'email': user.email,
            'is_head': user.is_admin,
            'department_name': user.department.name
        })


@api_view([HTTPMethod.post])
def verify_email(request):
    data = request.data
    code = random.randint(10000, 99999)
    teacher_email = data['email']
    email_body = f'Hello! Use this code below to verify your email\n{code}'
    email_data = {
        'email_body': email_body,
        'email_subject': 'Verify your email',
        'email_to': teacher_email
    }
    Util.send_email(email_data)
    data['code'] = code
    return Response(data)


@api_view([HTTPMethod.post])
def registration_view(request):
    serializer = TeacherSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        teacher = serializer.save()
        data['first_name'] = teacher.first_name
        data['second_name'] = teacher.second_name
        data['kpi'] = teacher.kpi
        data['position'] = teacher.position
        data['one_rate'] = teacher.one_rate
        data['username'] = teacher.username
        data['email'] = teacher.email
        data['token'] = Token.objects.get(user=teacher).key
        data['is_head'] = teacher.is_admin
        data['department_name'] = teacher.department.name
    else:
        data = serializer.errors
    return Response(data)
