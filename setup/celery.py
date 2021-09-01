from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
app = Celery('setup', broker="redis://localhost:6379", backend="redis://localhost:6379")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {

    # ALERTA
    'alerta': {
        'task': 'core.tasks.processa_alerta',
        'schedule': 1,
        "args": ("request", 0)
    },

    #EMAIL
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