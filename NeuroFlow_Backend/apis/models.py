from django.db import models
from django.contrib.auth.models import User

import json


class FileData(models.Model):
    filename = models.CharField(max_length=255)
    sample_data = models.JSONField()
    column_data = models.JSONField()

    def __str__(self):
        return self.filename
<<<<<<< HEAD


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.username
=======
>>>>>>> merge_branch
