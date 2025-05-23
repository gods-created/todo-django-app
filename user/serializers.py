from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
)
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema_serializer
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict

@extend_schema_serializer(
    exclude_fields=('email', )
)
class AuthSerializer(ModelSerializer):
    class Meta:
        model = User 
        fields = 'username', 'email', 'password',

    def auth(self) -> dict:
        username, email, password = (
            self.validated_data.get('username'),
            self.validated_data.get('email'),
            self.validated_data.get('password')
        )

        if not (user := User.objects.prefetch_related('tasks').filter(username=username).first()):
            if not email:
                raise ValidationError(detail={'email': 'The \'email\' field is required.'})
            
            user = User.objects.create_user(username=username, password=password, email=email)
        
        if not check_password(password, user.password):
            raise ValidationError(detail={'password': 'Invalid password.'})
        
        refresh = RefreshToken().for_user(user=user)
        access_token = str(refresh.access_token)
        tasks = user.tasks.all()

        return {
            'user': model_to_dict(user),
            'tasks': [model_to_dict(task) for task in tasks] if tasks else [],
            'access_token': access_token
        }
