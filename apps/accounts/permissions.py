from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrSuperAdmin(BasePermission):
    """
    Allows full access to Manager and SuperAdmin users.
    Standard users can only read safe methods.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_manager() or request.user.is_superadmin()


class IsSuperAdminOnly(BasePermission):
    """
    Allows access only to SuperAdmin users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superadmin()
        )