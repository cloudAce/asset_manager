from django.contrib import admin

from apps.assets.models import (
    Asset,
    AssetActivityLog,
    AssetAssignment,
    AssetMaintenanceLog,
    Location,
)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "building",
        "floor",
        "room",
        "created_at",
    )
    search_fields = (
        "name",
        "building",
        "floor",
        "room",
    )
    list_filter = (
        "building",
        "floor",
    )


class AssetAssignmentInline(admin.TabularInline):
    model = AssetAssignment
    extra = 0
    autocomplete_fields = (
        "assigned_to",
        "assigned_by",
    )
    readonly_fields = (
        "assigned_at",
    )


class AssetMaintenanceLogInline(admin.TabularInline):
    model = AssetMaintenanceLog
    extra = 0
    autocomplete_fields = (
        "reported_by",
    )
    readonly_fields = (
        "started_at",
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "asset_tag",
        "name",
        "category",
        "status",
        "condition",
        "location",
        "created_at",
    )

    list_filter = (
        "status",
        "condition",
        "category",
        "location",
        "created_at",
    )

    search_fields = (
        "asset_tag",
        "name",
        "serial_number",
        "manufacturer",
        "model_number",
    )

    readonly_fields = (
        "id",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "location",
    )

    inlines = (
        AssetAssignmentInline,
        AssetMaintenanceLogInline,
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "assigned_to",
        "assigned_by",
        "assigned_at",
        "expected_return_at",
        "returned_at",
    )

    list_filter = (
        "assigned_at",
        "returned_at",
    )

    search_fields = (
        "asset__asset_tag",
        "asset__name",
        "assigned_to__username",
    )

    autocomplete_fields = (
        "asset",
        "assigned_to",
        "assigned_by",
    )


@admin.register(AssetMaintenanceLog)
class AssetMaintenanceLogAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "issue_title",
        "status",
        "repair_cost",
        "started_at",
        "resolved_at",
    )

    list_filter = (
        "status",
        "started_at",
        "resolved_at",
    )

    search_fields = (
        "asset__asset_tag",
        "asset__name",
        "issue_title",
    )

    autocomplete_fields = (
        "asset",
        "reported_by",
    )


@admin.register(AssetActivityLog)
class AssetActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "event_type",
        "actor",
        "created_at",
    )

    list_filter = (
        "event_type",
        "created_at",
    )

    search_fields = (
        "asset__asset_tag",
        "asset__name",
        "actor__username",
        "message",
    )

    autocomplete_fields = (
        "asset",
        "actor",
    )

    readonly_fields = (
        "created_at",
    )