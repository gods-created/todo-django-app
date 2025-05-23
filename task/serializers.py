from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    CharField,
    DateTimeField,
    ValidationError
)

from .models import Task
from user.models import User
from drf_spectacular.utils import extend_schema_serializer
from django.forms.models import model_to_dict
from django.db.models import Q
from django_celery_beat.models import (
    ClockedSchedule,
    PeriodicTask
)
from json import loads, dumps

@extend_schema_serializer(
    exclude_fields=('user', )
)
class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = 'user', 'title', 'description', 'expired_time'

    user = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=False,
        required=False,
    )

    title = CharField(
        required=False,
        allow_blank=True,
        max_length=150
    )

    description = CharField(
        required=False,
        allow_blank=True,
    )

    expired_time = DateTimeField(
        required=False,
    )

    def get_tasks(self) -> list:
        user_id = self.validated_data.get('user')
        tasks = Task.objects.sort_by_exp(user_id=user_id) or []
        return tasks

    def create_task(self):
        data = self.validated_data
        if not len(data.keys()) == 4:
            raise ValidationError(detail={'error': f'The fields has to have filling'})
        
        for key, item in data.items():
            if not item:
                raise ValidationError(detail={key: f'The \'{key}\' can\'t to be empty'})

        task = Task.objects.create(**data)
        return {
            'task': model_to_dict(task)
        }
    
    def delete_task(self, task_id: int) -> dict:
        user_id = self.validated_data.get('user')
        _, *_ = Task.objects.filter(Q(user_id=user_id) & Q(id=task_id)).delete()
        periodic_task = PeriodicTask.objects.filter(description__icontains=f'"task_id": {task_id}').first()
        if periodic_task:
            periodic_task_description = loads(periodic_task.description)
            _, *_ = ClockedSchedule.objects.filter(pk=periodic_task_description['clocked_id']).delete()
            periodic_task.delete()

        return {}