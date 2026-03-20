
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Creates a superuser (idempotent).'

    def handle(self, *args, **options):
        username = os.getenv("SU_USERNAME", "admin")
        password = os.getenv("SU_PASSWORD", "admin")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists. Skipping.'))
            return

        print(f'Creating superuser | {username} | {password}')
        User.objects.create_superuser(username=username, password=password)
