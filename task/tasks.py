from celery import shared_task
from django.core.mail import send_mail
from os import getenv
from django_celery_beat.models import (
    ClockedSchedule,
    PeriodicTask
)
from .models import Task

@shared_task(name='task.tasks.send_notification', bind=True, queue='low_priority')
def send_notification(self, *args, **kwargs) -> None:
    try:
        subject, message, email = args

        send_mail(
            subject=subject,
            message=message,
            from_email=getenv('EMAIL_HOST_USER'),
            recipient_list=[email]
        )

        periodic_task, clocked_id, periodic_task_id, task_id = (
            kwargs.get('periodic_task'),
            kwargs.get('clocked_id'),
            kwargs.get('periodic_task_id'),
            kwargs.get('task_id')
        )

        if periodic_task:
            _, *_ = ClockedSchedule.objects.filter(pk=clocked_id).delete()
            _, *_ = PeriodicTask.objects.filter(pk=periodic_task_id).delete()
            _, *_ = Task.objects.filter(pk=task_id).delete()

    except Exception as e:
        self.retry(exc=str(e), countdown=5)
    
    return None