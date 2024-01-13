from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscribe


@admin.register(CustomUser)
class UsersAdmin(UserAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name")
    list_filter = ("username", "email")
    search_fields = ("username", "email")


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "author")
    # list_display_links = ('id', 'user')
    search_fields = ("user",)
