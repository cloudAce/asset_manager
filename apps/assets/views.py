from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsManagerOrSuperAdmin
from apps.assets.models import (
    Asset,
    AssetActivityLog,
    AssetAssignment,
    AssetMaintenanceLog,
    Location,
)
from apps.assets.serializers import (
    AssetActivityLogSerializer,
    AssetAssignmentSerializer,
    AssetMaintenanceLogSerializer,
    AssetSerializer,
    LocationSerializer,
)


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing locations.
    Managers and SuperAdmins can create/update/delete.
    Authenticated users can view.
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsManagerOrSuperAdmin]
    search_fields = ["name", "building", "floor", "room"]
    ordering_fields = ["name", "created_at"]


class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing assets.
    Managers and SuperAdmins can create/update/delete.
    Authenticated users can view.
    """

    serializer_class = AssetSerializer
    permission_classes = [IsManagerOrSuperAdmin]
    search_fields = [
        "asset_tag",
        "name",
        "category",
        "manufacturer",
        "model_number",
        "serial_number",
    ]
    ordering_fields = [
        "asset_tag",
        "name",
        "category",
        "status",
        "condition",
        "created_at",
    ]

    def get_queryset(self):
        return Asset.objects.select_related(
            "location",
            "created_by",
            "updated_by",
        ).all()

    def perform_create(self, serializer):
        asset = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        AssetActivityLog.objects.create(
            asset=asset,
            event_type=AssetActivityLog.EventType.CREATED,
            actor=self.request.user,
            message=f"Asset {asset.asset_tag} was created.",
            metadata={
                "status": asset.status,
                "condition": asset.condition,
            },
        )

    def perform_update(self, serializer):
        asset = serializer.save(updated_by=self.request.user)

        AssetActivityLog.objects.create(
            asset=asset,
            event_type=AssetActivityLog.EventType.UPDATED,
            actor=self.request.user,
            message=f"Asset {asset.asset_tag} was updated.",
            metadata={
                "status": asset.status,
                "condition": asset.condition,
            },
        )


class AssetAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for assigning assets to users.
    """

    serializer_class = AssetAssignmentSerializer
    permission_classes = [IsManagerOrSuperAdmin]
    search_fields = [
        "asset__asset_tag",
        "asset__name",
        "assigned_to__username",
        "assigned_to__email",
    ]
    ordering_fields = [
        "assigned_at",
        "expected_return_at",
        "returned_at",
    ]

    def get_queryset(self):
        return AssetAssignment.objects.select_related(
            "asset",
            "assigned_to",
            "assigned_by",
        ).all()

    def perform_create(self, serializer):
        assignment = serializer.save(assigned_by=self.request.user)

        assignment.asset.status = Asset.Status.ASSIGNED
        assignment.asset.updated_by = self.request.user
        assignment.asset.save(update_fields=["status", "updated_by", "updated_at"])

        AssetActivityLog.objects.create(
            asset=assignment.asset,
            event_type=AssetActivityLog.EventType.ASSIGNED,
            actor=self.request.user,
            message=(
                f"Asset {assignment.asset.asset_tag} was assigned to "
                f"{assignment.assigned_to.username}."
            ),
            metadata={
                "assigned_to": assignment.assigned_to.username,
            },
        )


class AssetMaintenanceLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for maintenance logs.
    """

    serializer_class = AssetMaintenanceLogSerializer
    permission_classes = [IsManagerOrSuperAdmin]
    search_fields = [
        "asset__asset_tag",
        "asset__name",
        "issue_title",
        "issue_description",
    ]
    ordering_fields = [
        "started_at",
        "resolved_at",
        "repair_cost",
        "status",
    ]

    def get_queryset(self):
        return AssetMaintenanceLog.objects.select_related(
            "asset",
            "reported_by",
        ).all()

    def perform_create(self, serializer):
        maintenance_log = serializer.save(reported_by=self.request.user)

        maintenance_log.asset.status = Asset.Status.MAINTENANCE
        maintenance_log.asset.updated_by = self.request.user
        maintenance_log.asset.save(update_fields=["status", "updated_by", "updated_at"])

        AssetActivityLog.objects.create(
            asset=maintenance_log.asset,
            event_type=AssetActivityLog.EventType.MAINTENANCE,
            actor=self.request.user,
            message=f"Maintenance logged for {maintenance_log.asset.asset_tag}.",
            metadata={
                "issue_title": maintenance_log.issue_title,
                "maintenance_status": maintenance_log.status,
            },
        )


class AssetActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for asset activity logs.
    """

    serializer_class = AssetActivityLogSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        "asset__asset_tag",
        "asset__name",
        "actor__username",
        "message",
    ]
    ordering_fields = [
        "created_at",
        "event_type",
    ]

    def get_queryset(self):
        return AssetActivityLog.objects.select_related(
            "asset",
            "actor",
        ).all()