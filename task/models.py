from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    Index,
    CASCADE
)
from django.utils.timezone import now, timedelta
from .managers import TaskManager

class Task(Model):
    user = ForeignKey('user.User', related_name='tasks', on_delete=CASCADE)
    title = CharField(
        null=False,
        blank=False,
        max_length=150,
    )
    description = TextField(
        null=True,
        blank=True,
        default=''
    )
    created_at = DateTimeField(
        auto_now_add=True
    )
    expired_time = DateTimeField(
        null=False,
    )
    objects = TaskManager()

    class Meta:
        app_label = 'task'
        db_table = 'tasks'
        ordering = 'id', 'user_id', 'expired_time', 'created_at', 'title'
        indexes = (
            Index(fields=('user_id', 'expired_time')),
        )

    def save(self, *args, **kwargs):
        if not self.expired_time:
            self.expired_time = now() + timedelta(days=1)
        return super().save(*args, **kwargs)