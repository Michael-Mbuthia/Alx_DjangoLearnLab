"""Custom permission classes for the API.

These are used by ViewSets/Views via `permission_classes`.
"""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedReadOnlyOrAdminWrite(BasePermission):
    """Allow authenticated reads; require staff for writes.

    - SAFE methods (GET/HEAD/OPTIONS): any authenticated user
    - Write methods (POST/PUT/PATCH/DELETE): authenticated staff only
    """

    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS:
            return bool(user and user.is_authenticated)
        return bool(user and user.is_authenticated and user.is_staff)
