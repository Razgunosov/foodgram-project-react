from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView

from .services.filter import RecipeFilter, IngredientFilter
from .services.pagination import CustomPagination
from .services.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeShortSerializer,
    RecipeCreateSerializer,
    TagSerializer,
)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer


class ShopCartApiView(APIView):
    """Добавить или удалить рецепт в корзину"""

    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            return Response(
                {"errors": "Этот рецепт уже добавлен!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        shop_cart = ShoppingCart.objects.create(
            user=request.user, recipe=recipe
        )
        shop_cart.save()
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if not ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            return Response(
                {"errors": "Этот рецепт уже удалён!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        shop_cart = ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        )
        shop_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteApiView(APIView):
    """Добавить или удалить рецепт в избранное"""

    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            return Response(
                {"errors": "Этот рецепт уже добавлен!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        favorite = Favorite.objects.create(user=request.user, recipe=recipe)
        favorite.save()
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if not Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            return Response(
                {"errors": "Этот рецепт уже удалён!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShopingCartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        prefix = "Cписок покупок:"
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipes__shopping_cart__user=request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )
        for num, i in enumerate(ingredients):
            prefix += (
                f"\n{i['ingredient__name']} - "
                f"{i['amount']} {i['ingredient__measurement_unit']}"
            )
            if num < ingredients.count() - 1:
                prefix += ", "
        file = "shopping_list"
        response = HttpResponse(prefix, "Content-Type: application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{file}.pdf"'
        return response
