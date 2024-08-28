from rest_framework import permissions


class IsAuthorOrIsStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.post_author == request.user or request.user.is_staff
