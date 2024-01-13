from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator

from colorfield.fields import ColorField


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
        unique=True
    )
    color = ColorField(
        verbose_name="цвет",
        help_text="Введите код цвета в формате HEX",
        format='hex',
        default='#000000',
        unique=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=250,
    )
    measurement_unit = models.CharField(
        verbose_name="Еденица измерения",
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингридиенты",
        on_delete=models.CASCADE,
        related_name='ingredient_list',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1, message='Минимум - 1!')]
    )

    class Meta:
        default_related_name = 'ingridients_recipe'
        constraints = [
            UniqueConstraint(
                fields=('ingredient', 'amount'),
                name='unique_ingredient_in_recipe'),
        ]

    def __str__(self):
        return f'{self.ingredient} – {self.amount}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
        db_index=True
    )
    text = models.TextField(verbose_name="Текст",)
    image = models.ImageField(
        verbose_name="Изображение",
        blank=True,
        upload_to='recipes/images'
    )
    ingredients = models.ManyToManyField(
        IngredientInRecipe,
        verbose_name="Ингридиенты",
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Таг",
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Минимальное значение - 1')
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('user',)
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favourites',
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в избранное "{self.recipe}"'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в корзину "{self.recipe}"'
