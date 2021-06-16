# Generated by Django 3.2.3 on 2021-06-05 20:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0008_alter_art_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
