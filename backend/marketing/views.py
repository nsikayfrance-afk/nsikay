from rest_framework import viewsets
from .models import (
    Advertiser,
    AdvertisingCampaign,
    AdvertisementPlacement,
    Advertisement,
    AdvertisementStatistic
)
from .serializers import (
    AdvertiserSerializer,
    AdvertisingCampaignSerializer,
    AdvertisementPlacementSerializer,
    AdvertisementSerializer,
    AdvertisementStatisticSerializer
)


class AdvertiserViewSet(viewsets.ModelViewSet):
    queryset = Advertiser.objects.all()
    serializer_class = AdvertiserSerializer


class AdvertisingCampaignViewSet(viewsets.ModelViewSet):
    queryset = AdvertisingCampaign.objects.all()
    serializer_class = AdvertisingCampaignSerializer


class AdvertisementPlacementViewSet(viewsets.ModelViewSet):
    queryset = AdvertisementPlacement.objects.all()
    serializer_class = AdvertisementPlacementSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer


class AdvertisementStatisticViewSet(viewsets.ModelViewSet):
    queryset = AdvertisementStatistic.objects.all()
    serializer_class = AdvertisementStatisticSerializer

