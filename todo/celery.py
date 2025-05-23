from celery import Celery
from os import environ

environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

app = Celery('tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_routes = {
    'tasks.high_priority': {
        'queue': 'high_priority',
        'routing_key': 'high.#',
    },
    'tasks.low_priority': {
        'queue': 'low_priority',
        'routing_key': 'low.#',
    },
}
app.autodiscover_tasks()