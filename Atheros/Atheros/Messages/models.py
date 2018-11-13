from django.db import models
from django.contrib.postgres.fields import JSONField
from Workspaces.models import Channel
from Users.models import User
# Create your models here.


class Message(models.Model):

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channels = models.ForeignKey(Channel, on_delete=models.CASCADE)

class Replies(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
