from django.db import models

from django.conf import settings

from utils import get_file_path


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.FileField(upload_to=get_file_path, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author')
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked')
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} | {} | {}'.format(self.title, self.body, self.author.username)


# 1. get article
# 2. get user by article.author


# foreign key
# link to obj user
# 1. get article(author due to link)