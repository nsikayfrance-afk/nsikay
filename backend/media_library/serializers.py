from rest_framework import serializers
from .models import (
    MediaAsset,
    MediaDestination,
    MediaDistribution,
    MediaSegment,
)


class MediaDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaDestination
        fields = "__all__"


class MediaDistributionSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(
        source="destination.name",
        read_only=True
    )

    destination_code = serializers.CharField(
        source="destination.code",
        read_only=True
    )

    asset_title = serializers.CharField(
        source="asset.title",
        read_only=True
    )

    class Meta:
        model = MediaDistribution
        fields = "__all__"
        read_only_fields = [
            "created_by",
            "created_at",
            "updated_at",
            "started_at",
            "finished_at",
        ]


class MediaSegmentSerializer(serializers.ModelSerializer):
    destination_ids = serializers.PrimaryKeyRelatedField(
        source="destinations",
        many=True,
        queryset=MediaDestination.objects.filter(active=True),
        required=False
    )

    class Meta:
        model = MediaSegment
        fields = "__all__"


class MediaAssetSerializer(serializers.ModelSerializer):
    distributions = MediaDistributionSerializer(
        many=True,
        read_only=True
    )

    segments = MediaSegmentSerializer(
        many=True,
        read_only=True
    )

    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = "__all__"
        read_only_fields = [
            "owner",
            "created_at",
            "updated_at",
            "original_filename",
            "mime_type",
        ]

    def get_file_url(self, obj):
        if not obj.file:
            return ""
        request = self.context.get("request")
        url = obj.file.url
        return request.build_absolute_uri(url) if request else url

    def get_thumbnail_url(self, obj):
        if not obj.thumbnail:
            return ""
        request = self.context.get("request")
        url = obj.thumbnail.url
        return request.build_absolute_uri(url) if request else url
