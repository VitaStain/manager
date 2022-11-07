from celery import shared_task

from .service import send


@shared_task
def sample_task():
    send()
