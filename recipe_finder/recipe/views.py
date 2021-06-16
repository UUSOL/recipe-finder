from django.views import generic
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Art, Ingredient, Recipe
import json


def index(request):
    """View function for home page of the site."""

    arts_names = Art.objects.only('name')
    context = {
        'arts_names': arts_names
    }
    return render(request, 'index.html', context=context)


def choose_lifestyle(request):
    """View function for choose-lifestyle"""

    arts = Art.objects.all()
    context = {
        'arts': arts
    }
    return render(request, 'choose-lifestyle.html', context=context)


@csrf_exempt
def individual_lifestyle_detail(request, art):
    """View function for each lifestyle in detail."""

    art = Art.objects.get(name=art)
    context = {
        'art': art
    }

    if request.method == 'POST':
        request.session[art.name] = {'included': [], 'excluded': []}
        request.session.modified = True

    return render(request, 'individual_lifestyle_detail.html', context=context)


@csrf_exempt
def include_ingredients(request, art):
    """View function for each lifestyle for including ingredients."""

    _set_initial_if_not_present(request, art)

    if request.method == 'POST':
        request.session[art]['included'] = list(set(request.POST))
        request.session.modified = True

    included, excluded = request.session[art]['included'], request.session[art]['excluded']
    ingredients_to_render = Ingredient.objects.filter(~Q(name__in=excluded), art_id__name__exact=art)

    context = {
        'ingredients': ingredients_to_render,
        'art': art,
        'included': included
    }

    return render(request, 'include-ingredients.html', context=context)


@csrf_exempt
def exclude_ingredients(request, art):
    """View function for each lifestyle for excluding ingredients."""

    _set_initial_if_not_present(request, art)

    if request.method == 'POST':
        request.session[art]['excluded'] = list(set(request.POST))
        request.session.modified = True

    included, excluded = request.session[art]['included'], request.session[art]['excluded']

    ingredients_to_render = Ingredient.objects.filter(~Q(name__in=included), art_id__name__exact=art)

    context = {
        'ingredients': ingredients_to_render,
        'art': art,
        'excluded': excluded
    }

    return render(request, 'exclude-ingredients.html', context=context)


@csrf_exempt
def result_recipes(request, art):
    """View function for searching recipes in DB based on dynamic SQL query.

    Include ingredients will be searched with OR
    Exclude ingredients will be searched with AND
    """

    _set_initial_if_not_present(request, art)

    included, excluded = request.session[art]['included'], request.session[art]['excluded']

    include_ingredients_query = None
    exclude_ingredients_query = None

    if len(excluded) > 0:
        queries = [~Q(ingredients__icontains=ingredient) for ingredient in excluded]

        exclude_ingredients_query = queries.pop()
        for item in queries:
            exclude_ingredients_query &= item

    if len(included) > 0:
        queries = [Q(ingredients__icontains=ingredient) for ingredient in included]
        include_ingredients_query = queries.pop()
        for item in queries:
            include_ingredients_query |= item

    if include_ingredients_query and exclude_ingredients_query:
        recipes = Recipe.objects.filter(exclude_ingredients_query & include_ingredients_query, art_id__name__exact=art)
    elif include_ingredients_query:
        recipes = Recipe.objects.filter(include_ingredients_query, art_id__name__exact=art)
    elif exclude_ingredients_query:
        recipes = Recipe.objects.filter(exclude_ingredients_query, art_id__name__exact=art)
    else:
        recipes = Recipe.objects.filter(art_id__name__exact=art)

    context = {
        'recipes': recipes,
        'art': art
    }

    return render(request, 'result-recipes.html', context=context)


@login_required
def individual_user_recipes(request):
    """View function for logged user to see saved recipes"""

    user_recipes = Recipe.objects.filter(users__id=request.user.id)
    context = {
        'recipes': user_recipes
    }
    return render(request, 'user-cooking-book.html', context=context)


def signup(request):
    """View function for sign up build-in form"""

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def recipe_detail(request, art, pk):
    """View function for representing recipe in detail and save in the cooking book if user is authenticated"""

    recipe = Recipe.objects.filter(pk=pk, art_id__name__exact=art)
    is_exist = len(recipe)

    if not is_exist:
        return HttpResponseRedirect(f"/recipe/{art}-recipes")

    context = {
        'recipe': recipe[0],
        'art': art,
    }

    if request.method == 'GET':
        return render(request, './recipe/recipe_detail.html', context=context)

    if request.method == 'POST':
        if request.user.is_authenticated:
            recipe[0].users.add(request.user.id)
            return HttpResponseRedirect(f"/recipe/{art}-recipes")
        else:
            HttpResponseRedirect('login')


@login_required
@csrf_exempt
def user_recipe_detail(request, pk):
    """View function for representing saved individual recipe from user and delete button"""

    recipe = Recipe.objects.filter(pk=pk)
    is_exist = len(recipe)

    if not is_exist:
        return HttpResponseRedirect('/recipe/my-cooking-book')

    context = {
        'recipe': recipe[0],
    }

    if request.method == 'GET':
        return render(request, './user-recipe-detail.html', context=context)

    if request.method == 'POST':
        recipe[0].users.remove(request.user.id)
        return HttpResponseRedirect('/recipe/my-cooking-book')


def _set_initial_if_not_present(request, art):
    """Helper function to set up initial session."""

    choice = request.session.get(art, None)
    if choice is None:
        request.session[art] = {'included': [], 'excluded': []}
