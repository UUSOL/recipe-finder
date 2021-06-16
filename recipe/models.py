from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Art(models.Model):
    """Model representing an art of recipe. Vegan, Vegetarian etc for normalization"""
    LIFESTYLE = (
        ('VG', 'Vegan'),
        ('VT', 'Vegetarian'),
        ('DT', 'Diabetic'),
        ('AL', 'All'),
    )

    id = models.CharField(
        max_length=2,
        primary_key=True,
        choices=LIFESTYLE,
        help_text='Choose the nutrition style',
    )
    name = models.CharField(max_length=10, help_text='Enter a name for nutrition style')
    image = models.ImageField(upload_to='arts/', null=True, blank=True)
    description = models.TextField(max_length=1000, help_text='Enter a description for nutrition style', null=True)
    description_src = models.URLField(help_text='Enter an url for the source of description', null=True)

    def __str__(self):
        """String for representing the Model Art object."""
        return self.name


class Ingredient(models.Model):
    """Model representing the Model Ingredient object in normalized form."""
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='ingredients/', null=True, blank=True)
    art_id = models.ManyToManyField(Art, help_text='Select an Art for the ingredient')

    def __str__(self):
        """String for representing the Model Ingredient object."""
        return self.name

    def display_art_id(self):
        """Create a string for the Art. This is required to display art in Admin."""
        return ', '.join(art_id.name for art_id in self.art_id.all()[:3])

    display_art_id.short_description = 'Art'


class Recipe(models.Model):
    """Model representing the Model Recipe object in normalized form"""

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the the recipe')
    instruction = models.TextField(max_length=1500, help_text='Enter instructions for the cooking recipe ; separated')
    ingredients = models.TextField(max_length=1500, help_text='Enter ingredients for the cooking recipe ; separated')
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    recipe_src = models.URLField(help_text='Enter an url for the source of recipe', null=True, blank=True)
    art_id = models.ManyToManyField(Art, help_text='Select an Art for cooking recipe')
    ingredient = models.ManyToManyField(Ingredient, help_text='Select an ingredient for cooking recipe')
    users = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        """String for representing the Model Recipe object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this recipe."""
        return reverse('recipe-detail', args=[str(self.id)])

    def instructions_as_list(self):
        """Returns the instructions as list for templating in recipe_detail.html."""
        return self.instruction.split('; ')

    def ingredients_as_list(self):
        """Returns the ingredients as list for templating in recipe_detail.html"""
        return self.ingredients.split('; ')

    def display_art_id(self):
        """Create a string for the Art. This is required to display art in Admin."""
        return ', '.join(art_id.name for art_id in self.art_id.all()[:3])

    display_art_id.short_description = 'Art'


class Profile(models.Model):
    """Model for representing User with one to one relationship"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/', blank=True)
