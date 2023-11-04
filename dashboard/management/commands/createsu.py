
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        User.objects.filter(username='admin').delete()
        username = os.getenv("SU_USERNAME"),
        password = os.getenv("SU_PASSWORD")
        print(f'Creating superuser | {username} | {password}')
        User.objects.create_superuser(username=username, password=password)
