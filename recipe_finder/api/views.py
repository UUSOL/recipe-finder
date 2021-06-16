from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Recipes
from .serializers import RecipesSerializer
from django.views.decorators.csrf import csrf_exempt

# second version with api view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# third version with class based view
from rest_framework.views import APIView

# fourth version with generic
from rest_framework import generics
from rest_framework import mixins

# authentication with rest
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# viewsets
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Create your views here.
@csrf_exempt
def recipes_list(request):
    if request.method == 'GET':
        recipes = Recipes.objects.all()
        serializer = RecipesSerializer(recipes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RecipesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def recipe_detail(request, pk):
    try:
        recipe = Recipes.objects.get(pk=pk)
    except Recipes.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RecipesSerializer(recipe)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RecipesSerializer(recipe, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        recipe.delete()
        return HttpResponse(status=204)


# second version with api_view
@api_view(['GET', 'POST'])
def recipes_list_2(request):
    if request.method == 'GET':
        recipes = Recipes.objects.all()
        serializer = RecipesSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecipesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def recipe_detail_2(request, pk):
    try:
        recipe = Recipes.objects.get(pk=pk)
    except Recipes.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipesSerializer(recipe)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RecipesSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class based api view
class RecipesAPIView(APIView):

    def get(self, request):
        recipes = Recipes.objects.all()
        serializer = RecipesSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Recipes.objects.get(id=id)
        except Recipes.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        recipe = self.get_object(id)
        serializer = RecipesSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, id):
        recipe = self.get_object(id)
        serializer = RecipesSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = self.get_object(id)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class RecipeViewSet(viewsets.ViewSet):
    def list(self, request):
        recipes = Recipes.objects.all()
        serializer = RecipesSerializer(recipes, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RecipesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Recipes.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipesSerializer(recipe, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeGenericViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()


class RecipeModelViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
