from django.db import models
from Users.models import User
# Create your models here.

class Workspace(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.TextField()
    users = models.ManyToManyField(User)
    admin = models.ManyToManyField(User, related_name='admins')


class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    workspaces = models.ForeignKey(Workspace, on_delete=models.CASCADE)
