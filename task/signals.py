from django.db.models.signals import post_save
from .models import Task
from django.dispatch import receiver
from .tasks import send_notification as send_notification_task
from django_celery_beat.models import (
    ClockedSchedule,
    PeriodicTask
)
from textwrap import dedent
from json import dumps

@receiver(post_save, sender=Task)
def send_notification_if_task_created(instance, created, *args, **kwargs) -> None:
    if not created:
        return None
    
    pk, username, email, title, expired_time = (
        instance.pk,
        instance.user.username, 
        instance.user.email, 
        instance.title, 
        instance.expired_time
    )

    subject, message = (
        'ToDo: task time expired',
        dedent(text=f'''
            Hello, {username}! The time for executing your task with title \'{title}\' is expired.
        ''').strip()
    )

    clocked = ClockedSchedule.objects.create(clocked_time=expired_time)
    clocked_id = clocked.pk

    periodic_task = PeriodicTask.objects.create(
        clocked=clocked,
        name=title,
        one_off=True,
        task='task.tasks.send_notification',
        args='["{0}", "{1}", "{2}"]'.format(subject, message, email),
        queue='low_priority',
        enabled=True,
    )
    
    kwargs_data = dumps(
        {
            'periodic_task': True, 
            'clocked_id': clocked_id, 
            'periodic_task_id': periodic_task.pk,
            'task_id': pk
        }
    )

    periodic_task.description = kwargs_data
    periodic_task.kwargs = kwargs_data
    periodic_task.save()

    subject, message = (
        'ToDo: task created',
        dedent(text=f'''
            Hello, {username}! You created task with title \'{title}\' and it expired time is {expired_time}.
        ''').strip()
    )

    send_notification_task.apply_async(
        (subject, message, email,),
        queue='low_priority'
    )
