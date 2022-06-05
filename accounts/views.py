from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from accounts.models import Teacher
from api.model.static_models import HTTPMethod
from accounts.serializers import TeacherGETSerializer, TeacherSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from .utils import Util
import random
from rest_framework.permissions import IsAuthenticated


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        teacher = serializer.validated_data['user']
        Token.objects.get_or_create(user=teacher)
        serializer_get = TeacherGETSerializer(teacher=teacher)
        return Response(serializer_get.data)


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
        serializer_get = TeacherGETSerializer(teacher=teacher)
        data = serializer_get.data
    else:
        data = serializer.errors
    return Response(data)


@api_view([HTTPMethod.post])
@permission_classes([IsAuthenticated])
def change_kpi(request):
    teacher = Teacher.objects.get(
        username__exact=request.data['teacher_username'])
    teacher.kpi = request.data['kpi']
    teacher.one_rate = request.data['one_rate']
    teacher.save()
    serializer = TeacherGETSerializer(teacher=teacher)
    return Response(serializer.data)


@api_view([HTTPMethod.post])
@permission_classes([IsAuthenticated])
def change_load(request):
    teacher = Teacher.objects.get(
        username__exact=request.data['teacher_username'])
    teacher.load = request.data['load']
    teacher.save()
    serializer = TeacherGETSerializer(teacher=teacher)
    return Response(serializer.data)


@api_view([HTTPMethod.post])
@permission_classes([IsAuthenticated])
def change_password(request):
    teacher = Teacher.objects.get(
        username__exact=request.data['teacher_username'])
    # request.data['password']
    return Response({'success': True})
