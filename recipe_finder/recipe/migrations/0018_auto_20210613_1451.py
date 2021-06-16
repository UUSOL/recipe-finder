# Generated by Django 3.2.3 on 2021-06-13 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0017_rename_description_src_recipe_recipe_src'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(help_text='Enter ingredients for the cooking recipe ; separated', max_length=1500),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='instruction',
            field=models.TextField(help_text='Enter instructions for the cooking recipe ; separated', max_length=1500),
        ),
    ]