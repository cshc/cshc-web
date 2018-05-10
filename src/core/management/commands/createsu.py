"""
This command provides a way of creating a Django Super User without requiring
input on the console. 

NOTE: This command relies on the following environment variables being set:

SUPERUSER_EMAIL - the email address of the superuser
SUPERUSER_PASSWORD - the password for the superuser
"""
import os
from django.core.management.base import BaseCommand
from core.models import CshcUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = os.environ['SUPERUSER_EMAIL']
        password = os.environ['SUPERUSER_PASSWORD']
        if not CshcUser.objects.filter(email=email).exists():
            CshcUser.objects.create_superuser(email, password)
