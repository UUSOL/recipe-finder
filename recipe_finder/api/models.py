from django.db import models


class Recipes(models.Model):
    """Model representing the Model Recipe object in normalized form)"""
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the the recipe')
    instruction = models.TextField(max_length=1000, help_text='Enter instructions for the cooking recipe ; separated')
    ingredients = models.TextField(max_length=1000, help_text='Enter ingredients for the cooking recipe ; separated')

    def __str__(self):
        """String for representing the Model Recipe object."""
        return self.title
