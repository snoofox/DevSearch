# Generated by Django 4.0.5 on 2022-07-06 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_social_stackoverflow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='social_youtube',
        ),
    ]
