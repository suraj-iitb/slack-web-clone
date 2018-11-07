from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

import json
# Create your models here.

class users(models.Model):

    id = models.AutoField(primary_key=True)
    email = models.TextField()
    password = models.CharField(max_length=256)
    workspaces = JSONField(default=None)
