"""Celery configuration.
"""
from __future__ import absolute_import, print_function, unicode_literals
import os

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arkive.settings')

app = Celery('arkive', broker='redis://redis/0')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# if __name__ == '__main__':
#     app.start()