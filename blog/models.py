from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return '{} | {}'.format(self.title, self.body)
