from rest_framework import permissions


class IsImageOwner(permissions.BasePermission):
    """
    Custom Permission Class
    Checks if logged user is owner of an image
    """
    def has_permission(self, request, view):
    	return request.user and request.user.is_authenticated and not request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user