from __future__ import absolute_import, unicode_literals

# Ceci permet de charger les configurations Celery au démarrage du projet Django
from .celery import app as celery_app

__all__ = ('celery_app',)
