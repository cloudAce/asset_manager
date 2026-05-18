from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAssetApiPermission(BasePermission):
    """
    Permission rules for the asset management API.

    - Authenticated users can read data.
    - Managers and SuperAdmins can create and update.
    - Only SuperAdmins can delete.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.method == "DELETE":
            return request.user.is_superadmin()

        return request.user.is_manager() or request.user.is_superadmin()


class IsManagerOrSuperAdmin(BasePermission):
    """
    Allows access only to Manager and SuperAdmin users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_manager()
                or request.user.is_superadmin()
            )
        )


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