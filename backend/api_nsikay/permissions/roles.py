from rest_framework.permissions import BasePermission



class IsNSIKAYAdmin(BasePermission):


    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            hasattr(
                request.user,
                "nsikay_role"
            )

            and

            request.user.nsikay_role.role == "ADMIN"

        )



class IsBankUser(BasePermission):


    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            hasattr(
                request.user,
                "nsikay_role"
            )

            and

            request.user.nsikay_role.role == "BANK"

        )



class IsAgentUser(BasePermission):


    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            hasattr(
                request.user,
                "nsikay_role"
            )

            and

            request.user.nsikay_role.role == "AGENT"

        )


