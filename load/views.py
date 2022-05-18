from django.http import JsonResponse
from rest_framework.decorators import api_view
from api.model.static_models import HTTPMethod
from api.model.serializers import GroupSubjectSerializer


@api_view([HTTPMethod.get])
def available_by_subject(request):
    serializer = GroupSubjectSerializer(by_subject=True)
    return JsonResponse(serializer.data, safe=False)


@api_view([HTTPMethod.get])
def available_by_group(request):
    serializer = GroupSubjectSerializer(by_group=True)
    return JsonResponse(serializer.data, safe=False)
