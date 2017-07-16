from django.db import models

from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='creator')

    def __str__(self):
        return '{} | {}'.format(self.title, self.creator)
