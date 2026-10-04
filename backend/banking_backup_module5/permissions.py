from django.contrib.auth.models import User


def is_bank_user(user):

    return hasattr(user, "bank_profile")


def is_admin_user(user):

    return user.is_staff


def can_access_bank_data(user, bank):

    if user.is_staff:
        return True

    if hasattr(user, "bank_profile"):

        return user.bank_profile == bank

    return False

