from rest_framework import serializers
from .models import (
    Advertiser,
    AdvertisingCampaign,
    AdvertisementPlacement,
    Advertisement,
    AdvertisementStatistic
)


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = '__all__'


class AdvertisingCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisingCampaign
        fields = '__all__'


class AdvertisementPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementPlacement
        fields = '__all__'


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'


class AdvertisementStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementStatistic
        fields = '__all__'

