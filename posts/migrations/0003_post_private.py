# Generated by Django 3.2.11 on 2022-01-22 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
