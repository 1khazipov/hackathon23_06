import time

from celery import shared_task

@shared_task
def ml_pipeline():
    time.sleep(20)
    print("completed")