from django.urls import path
from .views import auth

app_name = 'user'

urlpatterns = [
    path('auth/', auth, name='auth'),
]