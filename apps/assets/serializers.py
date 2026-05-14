from rest_framework import serializers

from apps.assets.models import (
    Asset,
    AssetActivityLog,
    AssetAssignment,
    AssetMaintenanceLog,
    Location,
)


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for asset locations."""

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "building",
            "floor",
            "room",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for hardware asset records."""

    location_name = serializers.CharField(source="location.name", read_only=True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    updated_by_username = serializers.CharField(source="updated_by.username", read_only=True)

    class Meta:
        model = Asset
        fields = [
            "id",
            "asset_tag",
            "name",
            "category",
            "manufacturer",
            "model_number",
            "serial_number",
            "status",
            "condition",
            "location",
            "location_name",
            "purchase_date",
            "warranty_expiration",
            "extra_details",
            "created_by",
            "created_by_username",
            "updated_by",
            "updated_by_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]


class AssetAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for asset assignment records."""

    asset_tag = serializers.CharField(source="asset.asset_tag", read_only=True)
    assigned_to_username = serializers.CharField(source="assigned_to.username", read_only=True)
    assigned_by_username = serializers.CharField(source="assigned_by.username", read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = AssetAssignment
        fields = [
            "id",
            "asset",
            "asset_tag",
            "assigned_to",
            "assigned_to_username",
            "assigned_by",
            "assigned_by_username",
            "assigned_at",
            "expected_return_at",
            "returned_at",
            "notes",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "assigned_by",
            "assigned_at",
            "is_active",
        ]


class AssetMaintenanceLogSerializer(serializers.ModelSerializer):
    """Serializer for maintenance and repair records."""

    asset_tag = serializers.CharField(source="asset.asset_tag", read_only=True)
    reported_by_username = serializers.CharField(source="reported_by.username", read_only=True)

    class Meta:
        model = AssetMaintenanceLog
        fields = [
            "id",
            "asset",
            "asset_tag",
            "reported_by",
            "reported_by_username",
            "issue_title",
            "issue_description",
            "status",
            "repair_cost",
            "started_at",
            "resolved_at",
        ]
        read_only_fields = [
            "id",
            "reported_by",
            "started_at",
        ]


class AssetActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for asset audit trail records."""

    asset_tag = serializers.CharField(source="asset.asset_tag", read_only=True)
    actor_username = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = AssetActivityLog
        fields = [
            "id",
            "asset",
            "asset_tag",
            "event_type",
            "actor",
            "actor_username",
            "message",
            "metadata",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "actor",
            "created_at",
        ]