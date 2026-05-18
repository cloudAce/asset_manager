from django.contrib.auth import get_user_model
from rest_framework import viewsets

from apps.accounts.permissions import IsManagerOrSuperAdmin
from apps.accounts.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for users.

    Managers and SuperAdmins can view users so they can assign assets properly.
    """

    serializer_class = UserSerializer
    permission_classes = [IsManagerOrSuperAdmin]
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "department",
    ]
    ordering_fields = [
        "username",
        "email",
        "date_joined",
    ]

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by("username")