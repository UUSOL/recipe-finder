# Generated by Django 3.2.3 on 2021-06-15 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0018_auto_20210613_1451'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IngredientNN',
        ),
        migrations.DeleteModel(
            name='RecipeNN',
        ),
    ]
