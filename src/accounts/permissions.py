from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Unauthorized: Not admin user.'

    def has_permission(self, request, view):
        return request.user.is_admin