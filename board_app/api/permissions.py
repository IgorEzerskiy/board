from rest_framework.permissions import BasePermission


class IsAuthenticatedOrPermissionDeny(BasePermission):
    message = 'Access denied. Login or register.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
