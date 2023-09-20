import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mueppbo_project.settings")
app = Celery("mueppbo_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-token-every-hour': {
        'task': 'sms_service.tasks.get_token',
        'schedule': crontab(minute='*/3'),
        'args': ('https://api.orange.com/oauth/v3/token',)
    }
}