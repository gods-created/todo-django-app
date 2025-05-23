#!/bin/sh

sleep 3

python manage.py migrate silk
python manage.py migrate user
python manage.py migrate task
python manage.py migrate django_celery_beat

python -m gunicorn todo.asgi:application \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8001 \
    --timeout 60 &

python -m celery -A todo.celery:app worker --queues=low_priority &
python -m celery -A todo.celery:app beat &

wait
# exec "$@"