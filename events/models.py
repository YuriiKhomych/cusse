from django.db import models

from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title
