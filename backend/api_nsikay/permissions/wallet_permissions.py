from rest_framework.permissions import BasePermission


class WalletAccessPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

