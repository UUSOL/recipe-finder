from django.test import TestCase
from .models import Art, Ingredient, Recipe
# Create your tests here.


class URLTests(TestCase):
    def test_recipe_urls(self):
        page_urls = ['signup', 'choose-lifestyle', 'vegan-lifestyle', 'vegetarian-lifestyle', 'diabetic-lifestyle',
                     'include-vegan-ingredients', 'include-vegetarian-ingredients', 'include-diabetic-ingredients',
                     'exclude-vegan-ingredients', 'exclude-vegetarian-ingredients', 'exclude-diabetic-ingredients',
                     'vegan-recipes', 'vegetarian-recipes', 'diabetic-recipes']

        for url in page_urls:
            response = self.client.get('/recipe/choose-lifestyle/')
            self.assertEqual(response.status_code, 200)


