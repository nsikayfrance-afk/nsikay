from rest_framework.permissions import BasePermission


class KYCVerifiedPermission(BasePermission):


    def has_permission(self, request, view):

        if not request.user.is_authenticated:

            return False


        try:

            return (
                request.user.kycprofile.status
                ==
                "VERIFIED"
            )

        except:

            return False


