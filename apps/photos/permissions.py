from rest_framework import permissions

from apps.accounts.models.profile import Profile


class CanListCreateRetrieveExpiringLink(permissions.BasePermission):
    def has_permission(self, request, view):
        profile = Profile.objects.get(user=request.user)
        return profile.account_tier.can_generate_expiring_links
