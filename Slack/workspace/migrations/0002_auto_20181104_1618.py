# Generated by Django 2.2.dev20181102145912 on 2018-11-04 16:18

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='channels',
            field=jsonfield.fields.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='workspace',
            name='users',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]
