"""api/permissions.py — Only couple users may access any resource."""
from rest_framework.permissions import BasePermission


class IsCoupleUser(BasePermission):
    """
    Allow access only to the two authenticated couple members.
    Since registration is already gated, any authenticated user is valid.
    """
    message = 'Access restricted to Love Journey members only.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
