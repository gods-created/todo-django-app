from django.urls import path
from .views import (
    create_task,
    get_tasks,
    delete_task
)

app_name = 'task'

urlpatterns = [
    path('create_task/', create_task, name='create_task'),
    path('delete_task/', delete_task, name='delete_task'),
    path('all/', get_tasks, name='get_tasks')
]
