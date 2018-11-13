# Generated by Django 2.0.5 on 2018-11-11 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_remove_user_workspaces'),
        ('Messages', '0002_message_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='replies',
        ),
        migrations.AddField(
            model_name='replies',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Messages.Message'),
        ),
        migrations.AddField(
            model_name='replies',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.User'),
        ),
    ]
