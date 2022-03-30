"""permissions for Store app."""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Check if logged-in user is a settings owner."""

    message = 'Logged-in user is not a Product owner.'

    def has_object_permission(self, request, view, obj):
        """Check if obj.user is request.user."""
        return request.user == obj.seller


class IsOwnerOrShowToAny(permissions.BasePermission):
    """Check if logged-in user is a Product owner or Cleint in Get Method."""

    message = 'Logged-in user is not a Product owner.'

    def has_object_permission(self, request, view, obj):
        """Check if obj.user is request.user."""
        if request.method == 'get':
            return True
        return request.user == obj.seller
