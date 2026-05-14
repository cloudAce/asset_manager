from rest_framework.routers import DefaultRouter

from apps.assets.views import (
    AssetActivityLogViewSet,
    AssetAssignmentViewSet,
    AssetMaintenanceLogViewSet,
    AssetViewSet,
    LocationViewSet,
)

router = DefaultRouter()
router.register("locations", LocationViewSet, basename="location")
router.register("assets", AssetViewSet, basename="asset")
router.register("assignments", AssetAssignmentViewSet, basename="asset-assignment")
router.register("maintenance-logs", AssetMaintenanceLogViewSet, basename="maintenance-log")
router.register("activity-logs", AssetActivityLogViewSet, basename="activity-log")

urlpatterns = router.urls