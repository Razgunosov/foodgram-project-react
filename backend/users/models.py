from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class UserRoles:
    USER = "user"
    ADMIN = "admin"
    choices = [(USER, "USER"), (ADMIN, "ADMIN")]


class CustomUser(AbstractUser):
    username = models.CharField(
        "Имя пользователя",
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        "Элетронная почта",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField("Имя", max_length=255, blank=True)
    last_name = models.CharField("Фамилия", max_length=255, blank=True)
    role = models.TextField(
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribing',
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            UniqueConstraint(fields=['user', 'author'],
                             name='unique_subscription')
        ]