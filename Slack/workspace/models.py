from django.db import models
from users import models as users_model
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Channel(models.Model):

     id = models.AutoField(primary_key=True)
     channel_name = models.CharField(max_length=20)
     users = JSONField(default=None)
     messages = JSONField(default=None)

class oneo1(models.Model):

    id = models.AutoField(primary_key=True)
    useroneo = models.CharField(max_length=20, default="")
    usertwoo = models.CharField(max_length=20, default="")
    messages = JSONField(default=None)

class workspace(models.Model):

    id = models.AutoField(primary_key=True)
    workspace_name = models.CharField(max_length=20)
    users = JSONField(default=None)
    channels = JSONField(default=None)
