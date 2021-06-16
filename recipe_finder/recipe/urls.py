from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('choose-lifestyle/', views.choose_lifestyle, name='choose-lifestyle'),
    re_path(r'^(vegan|vegetarian|diabetic|all)-lifestyle/$',
            views.individual_lifestyle_detail),
    re_path(r'^include-(vegan|vegetarian|diabetic|all)-ingredients/$',
            views.include_ingredients),
    re_path(r'^exclude-(vegan|vegetarian|diabetic|all)-ingredients/$',
            views.exclude_ingredients),
    re_path(r'^(vegan|vegetarian|diabetic|all)-recipes/$',
            views.result_recipes),
    re_path(r'^(?P<art>(vegan|vegetarian|diabetic|all))-recipes/(?P<pk>[0-9]+)/$',
            views.recipe_detail),
    path('my-cooking-book/<int:pk>', views.user_recipe_detail),
    path('my-cooking-book/', views.individual_user_recipes, name='my-cooking-book'),
]
