from django.core.management.base import BaseCommand

from accounts.models import User

from utils import random_word


class Command(BaseCommand):
    help = 'Create users'

    def handle(self, *args, **options):
        for item in range(100):
            User.objects.create(
                password=random_word(5),
                username=random_word(6),
                email='@'.join((random_word(6), 'gmail.com'))
            )
