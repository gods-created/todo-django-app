from django.db.models import (
    CharField
)
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_permissions=None 
    groups=None 

    username = CharField(
        null=False,
        blank=False,
        max_length=150,
        unique=False
    )

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'user'
        db_table = 'users'
        ordering = ['id', 'username', 'email', 'date_joined']
        indexes = ()

    def __str__(self):
        return self.username