from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab  
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

# pass the project name into it
celery_app = Celery('website')

# Using a string here means the worker doesn't have to serialize  
# the configuration object to child processes.  
# - namespace='CELERY' means all celery-related configuration keys  
#   should have a `CELERY_` prefix.  
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

#Celery Beat Settings  
celery_app.conf.beat_schedule = {  
    'send-mail-every-day-at-8' :  {  
        'task': 'emailExample.tasks.send_mail_func',  
        'schedule': crontab(hour = 15, minute = 42),  
        }
    }  

celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
