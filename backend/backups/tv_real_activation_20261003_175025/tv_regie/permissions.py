from rest_framework.permissions import BasePermission


class IsTVRegieOperator(BasePermission):
    """
    Autorise uniquement les utilisateurs certifiés régie TV.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.groups.filter(
                    name="TV_REGIE_OPERATOR"
                ).exists()
            )
        )

