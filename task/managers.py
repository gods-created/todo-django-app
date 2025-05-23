from django.db.models import Manager
from itertools import groupby

class TaskManager(Manager):
    def sort_by_exp(self, user_id) -> dict:
        items = self \
            .filter(user_id=user_id) \
            .values(
                'id',
                'title',
                'description',
                'created_at',
                'expired_time'
            ) \
            .order_by('-expired_time')
        
        if not items:
            return {}
        
        return {
            expired_time: list(each)
            for expired_time, each in 
            groupby(items, key=lambda x: str(x['expired_time']))
        }