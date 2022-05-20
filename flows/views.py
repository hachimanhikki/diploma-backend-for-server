from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from api.service.db_service import populate_database
from api.service.save_service import save_file
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.model.static_models import HTTPMethod


@csrf_exempt
@api_view([HTTPMethod.post])
def upload(request):
    if request.method == HTTPMethod.post:
        try:
            save_file(request.FILES[settings.UPLOADED_FILE_NAME])
            populate_database()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'message': e.message}, status=e.status)
    return Response({'success': False, 'message': 'File is not uploaded'}, status=500)
