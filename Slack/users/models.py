from django.db import models
from jsonfield import JSONField
# Create your models here.

class users(models.Model):

    id = models.AutoField(primary_key=True)
    email = models.TextField()
    password = models.CharField(max_length=256)
    workspaces = JSONField(default=None)
