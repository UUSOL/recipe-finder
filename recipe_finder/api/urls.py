
from django.urls import path, include
from .views import recipes_list, recipe_detail, RecipesAPIView, RecipeDetailAPIView, GenericAPIView, RecipeViewSet

# rest
from rest_framework.routers import DefaultRouter
#
router = DefaultRouter()
router.register('', RecipeViewSet, basename='recipe')
#

urlpatterns = [
    path('viewsets', include(router.urls)),
    path('viewsets/<int:pk>', include(router.urls)),
    # path('', recipes_list),
    path('', RecipesAPIView.as_view()),
    # path('detail/<int:pk>/', recipe_detail),
    # path('detail/<int:pk>', RecipeDetailAPIView.as_view()),
    path('detail/<int:pk>', GenericAPIView.as_view()),
]
