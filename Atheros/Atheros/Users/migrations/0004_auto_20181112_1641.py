# Generated by Django 2.0.5 on 2018-11-12 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_user_isfirst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isfirst',
            field=models.BooleanField(default=False),
        ),
    ]
