"""permissions for accounts app."""
from rest_framework import permissions


class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
    """The request is authenticated as a user, or is a post request."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated


class IsSeller(permissions.IsAuthenticated):
    """The request is authenticated user if seller."""

    def has_permission(self, request, view):
        return request.user.has_perm('account.is_seller')


class IsBuyer(permissions.IsAuthenticated):
    """The request is authenticated user if seller."""

    def has_permission(self, request, view):
        return request.user.has_perm('account.is_buyer')
