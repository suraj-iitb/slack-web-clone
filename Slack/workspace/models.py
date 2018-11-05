from django.db import models
from jsonfield import JSONField

# Create your models here.

class workspace(models.Model):

    id = models.AutoField(primary_key=True)
    workspace_name = models.CharField(max_length=20)
    users = JSONField(default=None)
    channels = JSONField(default=None)

class Channel(models.Model):

     id = models.AutoField(primary_key=True)
     channel_name = models.CharField(max_length=20)
     users = JSONField(default=None)
     messages = JSONField(default=None)
