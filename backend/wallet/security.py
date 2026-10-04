
from decimal import Decimal


def verify_wallet_operation(wallet):

    if not wallet:
        return False

    return True



def check_kyc(user):

    if hasattr(user, "kyc_verified"):
        return user.kyc_verified

    return False



def authorize_withdraw(user, amount):

    if not check_kyc(user):

        return {
            "authorized": False,
            "reason": "KYC_REQUIRED"
        }


    return {
        "authorized": True,
        "amount": Decimal(amount)
    }



def create_security_event(wallet, action, details):

    return {
        "wallet": wallet.id,
        "action": action,
        "details": details,
        "status": "RECORDED"
    }


