from django.core.management.base import BaseCommand

from blog.models import Article

from utils import random_word


class Command(BaseCommand):
    help = 'Create articles'

    def handle(self, *args, **options):
        for x in range(100):
            print(x)
            Article.objects.create(title=random_word(5),
                                   body=random_word(10),
                                   author_id=1)
        print('Done')