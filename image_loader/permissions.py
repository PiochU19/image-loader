from rest_framework import permissions
from image_loader.plan.models import UserPlan
from django.core.exceptions import ObjectDoesNotExist


class IsImageOwner(permissions.BasePermission):
    """
    Custom Permission Class
    Checks if logged user is owner of an image
    """

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and not request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class HasAbilityToGenerateExpiringLinks(permissions.BasePermission):
    """
    Custom Permission Class
    Check if logged user has plan
    that allows him to generate expiring links
    """

    def has_permission(self, request, views):

        return (
            request.user
            and request.user.is_authenticated
            and not request.user.is_staff
            and UserPlan.objects.get(user=request.user).plan.ability_to_generate_expiring_links
        )