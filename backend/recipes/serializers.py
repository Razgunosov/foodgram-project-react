from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField

from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from users.serializers import CustomUserSerializer
from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeShortSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class IngredientInRecipeSerializer(ModelSerializer):
    id = ReadOnlyField(source="ingredient.id")
    name = ReadOnlyField(source="ingredient.name")
    measurement_unit = ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class IngredientInRecipeWriteSerializer(ModelSerializer):
    id = IntegerField(write_only=True)
    amount = IntegerField(required=True)
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "amount", "name", "measurement_unit")

    def get_measurement_unit(self, ingredient):
        measurement_unit = ingredient.ingredient.measurement_unit
        return measurement_unit

    def get_name(self, ingredient):
        name = ingredient.ingredient.name
        return name


class RecipeGetSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True)
    image = Base64ImageField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, recipe):
        request = self.context.get("request")
        if not request:
            return False
        user = request.user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get("request")
        if not request:
            return False
        user = request.user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=recipe).exists()


class RecipeCreateSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def validate_ingredients(self, value):
        ingredients_list = []
        for item in value:
            ingredient = get_object_or_404(Ingredient, id=item["id"])
            if ingredient in ingredients_list:
                raise ValidationError(
                    {"ingredients": "Ингридиенты не должны повторяться!"}
                )
            if int(item["amount"]) <= 0:
                raise ValidationError(
                    {"amount": "Выберите количество ингридиентов!"}
                )
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        if not value:
            raise ValidationError({"tags": "Выберите тег!"})
        tags_set = set(value)
        if len(value) != len(tags_set):
            raise ValidationError({"tags": "Теги должны быть уникальными!"})
        return value

    def create_ingredients_amounts(self, ingredients, recipe):
        for ingredient in ingredients:
            ing, _ = IngredientInRecipe.objects.get_or_create(
                ingredient=get_object_or_404(
                    Ingredient.objects.filter(id=ingredient["id"])
                ),
                amount=ingredient["amount"],
            )
            recipe.ingredients.add(ing.id)

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_amounts(recipe=recipe, ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_amounts(
            recipe=instance, ingredients=ingredients
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return RecipeGetSerializer(instance, context=context).data
