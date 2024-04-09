from django.db import models
import json


class FileData(models.Model):
    filename = models.CharField(max_length=255)
    sample_data = models.JSONField()
    column_data = models.JSONField()

    def __str__(self):
        return self.filename

