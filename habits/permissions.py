from rest_framework import permissions


class IsOwnerOrReadOnlyForPublic(permissions.BasePermission):
    """
    Разрешения для модели с полем `owner` и флагом `is_public`.

    Правила:
    - Любой пользователь может читать объекты, если `is_public=True`.
    - Владельцу разрешены все действия (CRUD).
    - Остальные действия для других пользователей запрещены.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы для публичных объектов
        if request.method in permissions.SAFE_METHODS and getattr(obj, "is_public", False):
            return True

        # Разрешаем полные действия владельцу
        return getattr(obj, "owner", None) == request.user
