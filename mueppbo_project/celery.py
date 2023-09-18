import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mueppbo_project.settings")
app = Celery("mueppbo_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()