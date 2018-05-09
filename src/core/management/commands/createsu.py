"""
This command provides a way of creating a Django Super User without requiring
input on the console. 

NOTE: The Super User's password should obviously be changed to something secure
      as soon as possible.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "admin")
