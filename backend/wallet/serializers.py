from rest_framework import serializers
from .models import (
    Wallet,
    WalletBalance,
    WalletTransaction,
    ExchangeRate,
    WalletSecurityEvent
)


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"



class WalletBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletBalance
        fields = "__all__"



class WalletTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletTransaction
        fields = "__all__"



class ExchangeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRate
        fields = "__all__"

