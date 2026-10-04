
from rest_framework import serializers
from wallet.models import WalletAuditLog


class WalletAuditSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletAuditLog
        fields = "__all__"


