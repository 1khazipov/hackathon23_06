import time
import os
from django.core.cache import cache

from celery import shared_task

def after_computed():
    pass

def compute():
    pass

@shared_task
def ml_pipeline(url, id, **kwargs):
    key = f'{id}_status'
    try:
        compute()
    except:
        cache.delete(key)

    time.sleep(15)
    cache.set(f'{id}_status', {'status':'ready'})