import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q


class Location(models.Model):
    """
    Stores the physical location of an asset.
    Example: IT Lab, Room 204, Storage Room, Admin Office.
    """

    name = models.CharField(max_length=150, unique=True)
    building = models.CharField(max_length=150, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    room = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    Main hardware/equipment record.
    This tracks the asset identity, status, condition, location, and audit info.
    """

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        ASSIGNED = "ASSIGNED", "Assigned"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        RETIRED = "RETIRED", "Retired"

    class Condition(models.TextChoices):
        NEW = "NEW", "New"
        GOOD = "GOOD", "Good"
        FAIR = "FAIR", "Fair"
        DAMAGED = "DAMAGED", "Damaged"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    asset_tag = models.CharField(
        max_length=80,
        unique=True,
        db_index=True,
        help_text="Unique company/school asset tag. Example: LAP-0001",
    )

    name = models.CharField(max_length=180)
    category = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Example: Laptop, Monitor, Printer, Router",
    )

    manufacturer = models.CharField(max_length=120, blank=True)
    model_number = models.CharField(max_length=120, blank=True)

    serial_number = models.CharField(
        max_length=160,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.AVAILABLE,
        db_index=True,
    )

    condition = models.CharField(
        max_length=30,
        choices=Condition.choices,
        default=Condition.GOOD,
        db_index=True,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="assets",
        null=True,
        blank=True,
    )

    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiration = models.DateField(null=True, blank=True)

    extra_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Extra flexible details like RAM, storage, CPU, OS, etc.",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assets_created",
        null=True,
        blank=True,
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assets_updated",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["asset_tag"]),
            models.Index(fields=["serial_number"]),
            models.Index(fields=["status", "category"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"


class AssetAssignment(models.Model):
    """
    Tracks who currently has an asset.
    Only one active assignment per asset is allowed.
    """

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="asset_assignments",
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="asset_assignments_created",
        null=True,
        blank=True,
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    expected_return_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-assigned_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["asset"],
                condition=Q(returned_at__isnull=True),
                name="unique_active_assignment_per_asset",
            )
        ]

    @property
    def is_active(self):
        return self.returned_at is None

    def __str__(self):
        return f"{self.asset.asset_tag} assigned to {self.assigned_to.username}"


class AssetMaintenanceLog(models.Model):
    """
    Stores maintenance or repair records for assets.
    """

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="maintenance_logs",
    )

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="maintenance_reports",
        null=True,
        blank=True,
    )

    issue_title = models.CharField(max_length=180)
    issue_description = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True,
    )

    repair_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    started_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.issue_title}"


class AssetActivityLog(models.Model):
    """
    Audit trail for important asset actions.
    Example: created, updated, assigned, returned, marked for maintenance.
    """

    class EventType(models.TextChoices):
        CREATED = "CREATED", "Created"
        UPDATED = "UPDATED", "Updated"
        ASSIGNED = "ASSIGNED", "Assigned"
        RETURNED = "RETURNED", "Returned"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        RETIRED = "RETIRED", "Retired"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="activity_logs",
    )

    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices,
        db_index=True,
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="asset_activity_logs",
        null=True,
        blank=True,
    )

    message = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.event_type}"