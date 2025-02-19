from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définissez le module de configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoscoutapi.settings')

# Initialiser Celery
app = Celery('autoscoutapi')

# Charger les configurations de Django pour Celery
app.config_from_object("django.conf:settings", namespace='CELERY')
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

# Rechercher automatiquement les tâches définies dans les applications Django
app.autodiscover_tasks()

# FICHIER __INIT__.PY tres important pour que les tâches se mettent en db