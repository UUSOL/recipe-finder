from django.contrib import admin
from .models import Art, Ingredient, Recipe, Profile


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_art_id')
    list_filter = ('name', 'art_id')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_art_id')
    list_filter = ('name', 'art_id')
    fieldsets = (
        ('Recipe Title Section', {
            'fields': ('name', 'art_id', 'image')
        }),
        ('Recipe Main Information Section', {
            'fields': ('description', 'instruction', 'recipe_src')
        }),
        ('Ingredients Section', {
            'fields': ('ingredients', 'ingredient')
        }),
        #
        ('Users Section', {
            'fields': ('users', )
        }),
        #
    )


admin.site.register(Profile)
