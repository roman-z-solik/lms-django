from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Права доступа для модераторов
    Модератор может просматривать и редактировать, но не может создавать и удалять
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):
    """
    Права доступа для владельца объекта
    Пользователь может работать только со своими объектами
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdminUser(BasePermission):
    """
    Права доступа для администраторов
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSuperUser(BasePermission):
    """
    Права доступа для суперпользователей
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsModeratorOrReadOnly(BasePermission):
    """
    Модератор может редактировать, остальные только читать
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return request.user.groups.filter(name='moderators').exists()


class IsOwnerOrModerator(BasePermission):
    """
    Владелец или модератор могут работать с объектом
    """

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user

        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user

        return False


class IsAdminOrModerator(BasePermission):
    """
    Администратор или модератор
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or request.user.groups.filter(name='moderators').exists())
        )


class IsAuthenticatedAndReadOnly(BasePermission):
    """
    Только чтение для аутентифицированных пользователей
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.method in ['GET', 'HEAD', 'OPTIONS']
