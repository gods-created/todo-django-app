from adrf.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
    throttle_classes
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter
from asgiref.sync import sync_to_async
from .serializers import TaskSerializer

@extend_schema(
    request=TaskSerializer
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
async def get_tasks(request) -> Response:
    user = request.user
    if not user.is_authenticated:
        return Response(
            status=status.HTTP_200_OK,
            data=[]
        )
        
    data = request.data
    data['user'] = user.pk
    serializer = TaskSerializer(data=data)
    await sync_to_async(serializer.is_valid)(raise_exception=True)
    tasks = await sync_to_async(serializer.get_tasks)()
    return Response(
        status=status.HTTP_200_OK,
        data=tasks
    )

@extend_schema(
    request=TaskSerializer
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@throttle_classes([UserRateThrottle])
async def create_task(request) -> Response:
    user = request.user
    data = request.data
    data['user'] = user.pk
    serializer = TaskSerializer(data=data)
    await sync_to_async(serializer.is_valid)(raise_exception=True)
    create_task_response = await sync_to_async(serializer.create_task)()
    return Response(
        status=status.HTTP_201_CREATED,
        data=create_task_response
    )
    
@extend_schema(
    request=TaskSerializer,
    parameters=[
        OpenApiParameter(
            name='id',
            type=int,
            required=True
        )
    ]
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@throttle_classes([UserRateThrottle])
async def delete_task(request) -> Response:
    task_id = request.GET.get('id')
    if not task_id:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'id': 'The \'\' field can\'t to be empty'}
        )

    user = request.user
    data = request.data
    data['user'] = user.pk
    serializer = TaskSerializer(data=data)
    await sync_to_async(serializer.is_valid)(raise_exception=True)
    delete_task_response = await sync_to_async(serializer.delete_task)(task_id=task_id)
    return Response(
        status=status.HTTP_201_CREATED,
        data=delete_task_response
    )