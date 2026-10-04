from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AdvertiserViewSet,
    AdvertisingCampaignViewSet,
    AdvertisementPlacementViewSet,
    AdvertisementViewSet,
    AdvertisementStatisticViewSet
)

router = DefaultRouter()

router.register('advertisers', AdvertiserViewSet)
router.register('campaigns', AdvertisingCampaignViewSet)
router.register('placements', AdvertisementPlacementViewSet)
router.register('advertisements', AdvertisementViewSet)
router.register('statistics', AdvertisementStatisticViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

