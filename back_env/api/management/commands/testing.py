from django.core.management.base import BaseCommand
from ... import admanagement

class Command(BaseCommand):

    def handle(self, *args, **options):
        admanagement.testing()
