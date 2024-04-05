from django.db import models
import json


class FileSampleData(models.Model):
    filename = models.CharField(max_length=255)
    data_dict = models.JSONField()

    def __str__(self):
        return self.filename

