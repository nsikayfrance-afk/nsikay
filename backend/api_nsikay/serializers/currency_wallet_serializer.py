from rest_framework import serializers
from wallet.currency_models import WalletCurrencyBalance


class WalletCurrencyBalanceSerializer(serializers.ModelSerializer):

    class Meta:

        model = WalletCurrencyBalance

        fields = "__all__"

