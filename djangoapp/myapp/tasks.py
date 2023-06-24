import time
import os
from django.core.cache import cache
from .main import ml_entry

from celery import shared_task

def after_computed():
    pass

def compute(url):
    pass

#@shared_task
def ml_pipeline(source, id, **kwargs):
    key = f'{id}_status'
    try:
        text, frames = ml_entry(source, id)
    except:
        #todo: release temp
        cache.delete(key)

    cache.set(f'{id}_status', {'status':'ready'})