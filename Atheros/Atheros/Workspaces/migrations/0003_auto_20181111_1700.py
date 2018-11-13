# Generated by Django 2.0.5 on 2018-11-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_remove_user_workspaces'),
        ('Workspaces', '0002_auto_20181111_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='admin',
            field=models.ManyToManyField(related_name='admins', to='Users.User'),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='users',
            field=models.ManyToManyField(related_name='users', to='Users.User'),
        ),
    ]
