from adrf.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
    throttle_classes
)
from drf_spectacular.utils import extend_schema
from asgiref.sync import sync_to_async
from .serializers import AuthSerializer

@extend_schema(
    request=AuthSerializer
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
@throttle_classes([])
async def auth(request) -> Response:
    data = request.data
    serializer = AuthSerializer(data=data)
    await sync_to_async(serializer.is_valid)(raise_exception=True)

    auth_response = await sync_to_async(serializer.auth)()

    return Response(
        status=status.HTTP_200_OK,
        data=auth_response
    )
