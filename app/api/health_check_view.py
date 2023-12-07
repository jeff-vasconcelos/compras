from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def health_check(request):
    data = {
        'status': 'OK',
        'message': 'The API is healthy!',
    }

    try:
        connection.ensure_connection()
        return Response(data, status=200)

    except Exception as e:
        return Response({'message': str(e)}, status=500)
