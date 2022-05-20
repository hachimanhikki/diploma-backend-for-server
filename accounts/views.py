from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from api.model.static_models import HTTPMethod
from accounts.serializers import TeacherSerializer


@api_view([HTTPMethod.post])
def registration_view(request):
    if request.method == HTTPMethod.post:
        serializer = TeacherSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            teacher = serializer.save()
            data['response'] = 'succesfully registered a new user'
            data['email'] = teacher.email
            data['first_name'] = teacher.first_name
            data['second_name'] = teacher.second_name
            token = Token.objects.get(user=teacher).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
