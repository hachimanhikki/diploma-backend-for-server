from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from api.service.save_service import save_file
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.model.static_models import HTTPMethod
from api.model.error import IncorrectFileType


@csrf_exempt
@api_view([HTTPMethod.post])
def upload(request):
    if request.method == HTTPMethod.post:
        try:
            save_file(request.FILES[settings.SCHEDULE_FILE_NAME])
            # configureSchedule()
            return Response({'success': True})
        except IncorrectFileType as e:
            return Response({'message': e.message}, status=e.status)
        except Exception as e:
            return Response({'message': "Error"}, status=400)
    return Response({'message': 'File is not uploaded'}, status=500)
