from rest_framework.routers import DefaultRouter

from .views import (
    MediaAssetViewSet,
    MediaDestinationViewSet,
    MediaDistributionViewSet,
    MediaSegmentViewSet,
)

router = DefaultRouter()

router.register(
    r"assets",
    MediaAssetViewSet,
    basename="media-asset"
)

router.register(
    r"destinations",
    MediaDestinationViewSet,
    basename="media-destination"
)

router.register(
    r"distributions",
    MediaDistributionViewSet,
    basename="media-distribution"
)

router.register(
    r"segments",
    MediaSegmentViewSet,
    basename="media-segment"
)

urlpatterns = router.urls
