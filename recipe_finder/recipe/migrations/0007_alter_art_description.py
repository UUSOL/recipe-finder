# Generated by Django 3.2.3 on 2021-05-30 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_auto_20210530_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='art',
            name='description',
            field=models.TextField(help_text='Enter a description for nutrition style', max_length=500, null=True),
        ),
    ]
