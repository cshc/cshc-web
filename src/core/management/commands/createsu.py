"""
This command provides a way of creating a Django Super User without requiring
input on the console. 

NOTE: This command relies on the following environment variables being set:

SUPERUSER_EMAIL - the email address of the superuser
SUPERUSER_PASSWORD - the password for the superuser
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        username = 'admin'
        email = os.environ['SUPERUSER_EMAIL']
        password = os.environ['SUPERUSER_PASSWORD']
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
