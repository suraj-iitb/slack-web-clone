# Generated by Django 2.2.dev20181102145912 on 2018-11-06 11:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0005_auto_20181106_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='messages',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='channel',
            name='users',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='workspace',
            name='channels',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='workspace',
            name='users',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
        ),
    ]