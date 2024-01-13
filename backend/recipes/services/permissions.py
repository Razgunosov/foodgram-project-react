from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Если не админ, то имеет доступ только к get методам"""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_staff
        )


class IsAuthorOrReadOnly(BasePermission):
    """Редактировать и т.д. может только автор"""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
