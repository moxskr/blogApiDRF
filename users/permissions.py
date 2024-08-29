from rest_framework.permissions import BasePermission

ALLOWED_UNAUTHORIZED_USERS_METHODS = ['POST']


class UsersPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in ALLOWED_UNAUTHORIZED_USERS_METHODS
