from rest_framework import serializers

from wallet.models import WalletBankAccount



class WalletBankSerializer(serializers.ModelSerializer):


    class Meta:

        model = WalletBankAccount

        fields = "__all__"


