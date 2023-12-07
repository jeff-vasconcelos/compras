from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
app = Celery('setup')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {

    # ALERTA
    'alerta': {
        'task': 'core.tasks.processa_alerta',
        'schedule': 1,
        "args": ("request", 0)
    },

    # EMAIL
    'email': {
        'task': 'core.tasks.processa_email',
        'schedule': 1,
        "args": ("request", 0)
    },

}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
