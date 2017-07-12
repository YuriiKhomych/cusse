from django.db import models

from utils import get_file_path


class WebsiteConfiguration(models.Model):
    logo = models.FileField(upload_to=get_file_path)
    title = models.CharField(max_length=255)
    description = models.TextField()
