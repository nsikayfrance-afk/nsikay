from rest_framework import serializers


class WalletOperationSerializer(serializers.Serializer):

    wallet_id = serializers.IntegerField()

    amount = serializers.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    currency = serializers.CharField(
        max_length=10,
        default="USD"
    )

    destination_wallet_id = serializers.IntegerField(
        required=False
    )


