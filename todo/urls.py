from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('silk/', include('silk.urls', namespace='SILK')),
    path('error/', include('error.urls', namespace='error')),
    path('api/', include('api.urls', namespace='api')),
    path('user/', include('user.urls', namespace='user')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
