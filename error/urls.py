from django.urls import path
from .views import error404

app_name = 'error'

urlpatterns = [
    path('error404/', error404, name='error404'),
]