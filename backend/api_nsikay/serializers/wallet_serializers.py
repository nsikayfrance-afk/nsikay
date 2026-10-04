from rest_framework import serializers
from wallet.models import Wallet, WalletTransaction, WalletSecurityEvent


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"


class WalletTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletTransaction
        fields = "__all__"


class WalletSecurityEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletSecurityEvent
        fields = "__all__"

