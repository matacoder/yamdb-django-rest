from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    """
    Administrator permissions. Before this check,
    you need to check for authorization to avoid AttributeError
    """

    def has_permission(self, request, view):
        return request.user.is_admin


class AdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    Admin, Moderator, Owner or readonly permissions. Before this check,
    you need to check for authorization to avoid AttributeError
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)


class AdminOrReadOnly(permissions.BasePermission):
    """
    Admin or readonly permissions. Before this check,
    you need to check for authorization to avoid AttributeError
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)
