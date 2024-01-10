from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscribe


# class BaseAdminSettings(admin.ModelAdmin):
#     empty_value_display = '-empty-'
#     list_filter = ('email', 'username')


@admin.register(CustomUser)
class UsersAdmin(UserAdmin):
    list_display = (
        'id',
        'role',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_filter = ('username', 'email')
    # list_display_links = ('id', 'username', 'email')
    search_fields = ('role', 'username', 'email')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    # list_display_links = ('id', 'user')
    search_fields = ('user',) 


# admin.site.register(User, UsersAdmin)
# admin.site.register(Subscribe, SubscribeAdmin)