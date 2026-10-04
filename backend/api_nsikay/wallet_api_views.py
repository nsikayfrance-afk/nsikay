from rest_framework import generics
from wallet.models import Wallet, WalletTransaction, WalletSecurityEvent

from api_nsikay.serializers.wallet_serializers import (
    WalletSerializer,
    WalletTransactionSerializer,
    WalletSecurityEventSerializer
)

from api_nsikay.permissions.wallet_permissions import WalletAccessPermission



class WalletListAPIView(generics.ListAPIView):

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [WalletAccessPermission]



class WalletTransactionListAPIView(generics.ListAPIView):

    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer
    permission_classes = [WalletAccessPermission]



class WalletSecurityLogAPIView(generics.ListAPIView):

    queryset = WalletSecurityEvent.objects.all()
    serializer_class = WalletSecurityEventSerializer
    permission_classes = [WalletAccessPermission]

