# Generated by Django 3.2.3 on 2021-06-09 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_auto_20210609_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='art',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='arts/%name'),
        ),
    ]