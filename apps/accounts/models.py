from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for role-based access control.

    Roles:
    - SUPERADMIN: full system access
    - MANAGER: can manage assets
    - STANDARD_USER: regular user
    """

    class Role(models.TextChoices):
        SUPERADMIN = "SUPERADMIN", "Super Admin"
        MANAGER = "MANAGER", "Manager"
        STANDARD_USER = "STANDARD_USER", "Standard User"

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.STANDARD_USER,
    )

    department = models.CharField(max_length=120, blank=True)

    def is_superadmin(self):
        return self.role == self.Role.SUPERADMIN or self.is_superuser

    def is_manager(self):
        return self.role == self.Role.MANAGER

    def is_standard_user(self):
        return self.role == self.Role.STANDARD_USER