# Generated by Django 2.2.dev20181102145912 on 2018-11-06 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0004_auto_20181105_0524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='messages',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='users',
        ),
        migrations.RemoveField(
            model_name='workspace',
            name='channels',
        ),
        migrations.RemoveField(
            model_name='workspace',
            name='users',
        ),
    ]
