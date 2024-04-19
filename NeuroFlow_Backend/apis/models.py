from django.db import models
from django.contrib.auth.models import User

import json


class FileData(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    sample_data = models.JSONField()
    column_sum_data = models.JSONField()

    def __str__(self):
        return self.filename
