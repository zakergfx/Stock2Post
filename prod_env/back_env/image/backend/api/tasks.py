from celery import shared_task
from . import models
import os
from . import admanagement

@shared_task
def syncAutoscoutWithDb():
    admanagement.scheduledTask()