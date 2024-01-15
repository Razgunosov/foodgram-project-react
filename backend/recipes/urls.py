from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    DownloadShopingCartApiView,
    ShopCartApiView,
    FavoriteApiView,
)


app_name = "recipes"


router = DefaultRouter()


router.register("ingredients", IngredientViewSet)
router.register("tags", TagViewSet)
router.register("recipes", RecipeViewSet)


urlpatterns = [
    path(
        "recipes/download_shopping_cart/", DownloadShopingCartApiView.as_view()
    ),
    path("", include(router.urls)),
    path("recipes/<int:pk>/shopping_cart/", ShopCartApiView.as_view()),
    path("recipes/<int:pk>/favorite/", FavoriteApiView.as_view()),
]
