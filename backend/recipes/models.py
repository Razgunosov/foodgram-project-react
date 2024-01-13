from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(
        format="hex",
        default="#778899",
        unique=True,
    )
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ("slug",)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
    )
    measurement_unit = models.CharField(
        max_length=200,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_list",
    )
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1, "Не менее - 1")],
    )

    class Meta:
        default_related_name = "ingridients_recipe"
        constraints = [
            UniqueConstraint(
                fields=("ingredient", "amount"),
                name="unique_ingredient_in_recipe",
            ),
        ]

    def __str__(self):
        return f"{self.ingredient} – {self.amount}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name="recipes",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(blank=True, upload_to="recipes/images")
    text = models.TextField()
    ingredients = models.ManyToManyField(
        IngredientInRecipe,
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, "Не менее - 1")],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    class Meta:
        ordering = ("user",)
        constraints = [
            UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_favourites",
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart"
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в корзину'
