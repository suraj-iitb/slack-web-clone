from django.db import models
# Create your models here.

class User(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    isfirst = models.BooleanField(default=False)
