from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from api.model.static_models import HTTPMethod
from accounts.serializers import TeacherSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from config import settings


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
            token = Token.objects.get(user=teacher).key
            data['token'] = token
            data['is_head'] = teacher.is_admin
            data['department_name'] = teacher.department.name
        else:
            data = serializer.errors
        return Response(data)
