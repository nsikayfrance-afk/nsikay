
from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from api_nsikay.models import GiftTransaction, VirtualGift

from .models import FinancialAccount, GiftFinancialLedger


def get_gift_financial_account(currency):
    """
    Retourne le compte logique NSIKAY-GIFTS-[CURRENCY].
    Aucun compte bancaire réel n'est créé ici.
    """
    currency = (currency or "USD").upper()

    code = f"NSIKAY-GIFTS-{currency}"

    return FinancialAccount.objects.filter(
        code=code,
        currency=currency,
    ).first()


def make_reference(prefix, gift_transaction_id):
    return f"{prefix}-GIFT-TX-{gift_transaction_id}"


@receiver(post_save, sender=GiftTransaction)
def register_gift_financial_transaction(
    sender,
    instance,
    created,
    **kwargs
):
    """
    Trace financière automatique d'un envoi de cadeau.

    GiftTransaction reste le modèle métier principal.
    GiftFinancialLedger assure uniquement la traçabilité financière.

    Une transaction de cadeau produit :
      - SEND    : sortie logique du solde cadeau de l'expéditeur
      - RECEIVE : entrée logique du solde cadeau du bénéficiaire

    Aucune commission supplémentaire n'est prélevée ici.
    """

    if not created:
        return

    gift = instance.gift

    if not gift:
        return

    currency = (gift.currency or "USD").upper()
    amount = Decimal(str(gift.value))

    financial_account = get_gift_financial_account(currency)

    if financial_account is None:
        # On ne bloque jamais l'envoi du cadeau simplement parce
        # que le compte financier logique n'existe pas encore.
        return

    sender_reference = str(
        getattr(instance.sender, "username", None)
        or getattr(instance.sender, "pk", "")
    )

    receiver_reference = str(
        getattr(instance.receiver, "username", None)
        or getattr(instance.receiver, "pk", "")
    )

    # --------------------------------------------------------
    # SORTIE DU CADEAU CHEZ L'EXPEDITEUR
    # --------------------------------------------------------

    GiftFinancialLedger.objects.get_or_create(
        reference=make_reference("SEND", instance.pk),
        defaults={
            "operation_type": "SEND",
            "currency": currency,
            "amount": amount,
            "buyer_reference": "",
            "sender_reference": sender_reference,
            "beneficiary_reference": receiver_reference,
            "financial_account": financial_account,
            "related_reference": f"GIFT-TX-{instance.pk}",
        },
    )

    # --------------------------------------------------------
    # RECEPTION DU CADEAU CHEZ LE BENEFICIAIRE
    # --------------------------------------------------------

    GiftFinancialLedger.objects.get_or_create(
        reference=make_reference("RECEIVE", instance.pk),
        defaults={
            "operation_type": "RECEIVE",
            "currency": currency,
            "amount": amount,
            "buyer_reference": "",
            "sender_reference": sender_reference,
            "beneficiary_reference": receiver_reference,
            "financial_account": financial_account,
            "related_reference": f"GIFT-TX-{instance.pk}",
        },
    )
