from rest_framework import serializers
from ..models import TVChannel


class TVChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TVChannel
        fields="__all__"


