from decimal import Decimal
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from finance.models import Wallet
from finance.wallet_service import debit_wallet, credit_wallet
from financial_routing.services import calculate_fee

from .models import WenzeOrder, WenzeProduct


class WenzePaymentError(Exception):
    """Erreur métier liée au paiement WENZE."""


def pay_wenze_order_with_wallet(order, buyer_wallet):
    """
    Paie une commande WENZE avec un portefeuille NSIKAY.

    Cette opération :
    - verrouille la commande ;
    - vérifie que la commande appartient à l'acheteur ;
    - verrouille les portefeuilles ;
    - vérifie la devise ;
    - applique la commission WENZE de 0 % ;
    - débite l'acheteur ;
    - crédite le vendeur ;
    - enregistre les écritures WalletTransaction ;
    - passe la commande à PAID.
    """

    if order is None:
        raise WenzePaymentError("Commande WENZE introuvable.")

    if buyer_wallet is None:
        raise WenzePaymentError("Portefeuille acheteur introuvable.")

    with transaction.atomic():

        # ----------------------------------------------------
        # Verrouillage de la commande
        # ----------------------------------------------------

        locked_order = (
            WenzeOrder.objects
            .select_for_update()
            .select_related("product", "product__seller", "buyer")
            .filter(
                id=order.id,
                buyer=order.buyer,
            )
            .first()
        )

        if locked_order is None:
            raise WenzePaymentError(
                "La commande WENZE est introuvable ou n'appartient pas à l'acheteur."
            )

        if locked_order.status != "PENDING":
            raise WenzePaymentError(
                "Cette commande n'est pas en attente de paiement."
            )

        if locked_order.payment_method != "WALLET":
            raise WenzePaymentError(
                "Cette méthode concerne uniquement le portefeuille NSIKAY."
            )

        amount = Decimal(str(locked_order.total_amount))

        if amount <= Decimal("0.00"):
            raise WenzePaymentError(
                "Le montant de la commande doit être strictement positif."
            )

        # ----------------------------------------------------
        # Produit WENZE + stock
        # ----------------------------------------------------
        # Le produit est verrouillé pendant toute la transaction.
        # Le stock n'est donc jamais consommé avant le paiement.
        # ----------------------------------------------------

        locked_product = (
            WenzeProduct.objects
            .select_for_update()
            .filter(
                id=locked_order.product.id,
                status="ACTIVE",
            )
            .first()
        )

        if locked_product is None:
            raise WenzePaymentError(
                "Le produit WENZE est introuvable ou inactif."
            )

        quantity = int(locked_order.quantity)

        if quantity < 1:
            raise WenzePaymentError(
                "La quantité de la commande doit être strictement positive."
            )

        if locked_product.stock < quantity:
            raise WenzePaymentError(
                "Stock insuffisant pour cette commande."
            )

        # ----------------------------------------------------
        # Portefeuille acheteur
        # ----------------------------------------------------

        buyer_wallet_locked = (
            Wallet.objects
            .select_for_update()
            .select_related("currency", "user")
            .filter(
                id=buyer_wallet.id,
                user=locked_order.buyer,
                active=True,
            )
            .first()
        )

        if buyer_wallet_locked is None:
            raise WenzePaymentError(
                "Le portefeuille acheteur est introuvable ou inactif."
            )

        # ----------------------------------------------------
        # Portefeuille vendeur
        # IMPORTANT : même devise que la commande
        # ----------------------------------------------------

        seller_wallet = (
            Wallet.objects
            .select_for_update()
            .select_related("currency", "user")
            .filter(
                user=locked_order.product.seller,
                currency__code=locked_order.currency,
                active=True,
            )
            .first()
        )

        if seller_wallet is None:
            raise WenzePaymentError(
                "Le vendeur ne possède pas de portefeuille actif "
                "dans la devise de la commande."
            )

        # ----------------------------------------------------
        # Vérification des devises
        # ----------------------------------------------------

        buyer_currency = buyer_wallet_locked.currency.code
        seller_currency = seller_wallet.currency.code

        if buyer_currency != locked_order.currency:
            raise WenzePaymentError(
                "La devise du portefeuille acheteur ne correspond "
                "pas à la devise de la commande."
            )

        if seller_currency != locked_order.currency:
            raise WenzePaymentError(
                "La devise du portefeuille vendeur ne correspond "
                "pas à la devise de la commande."
            )

        if buyer_wallet_locked.id == seller_wallet.id:
            raise WenzePaymentError(
                "L'acheteur et le vendeur ne peuvent pas utiliser "
                "le même portefeuille."
            )

        # ----------------------------------------------------
        # Vérification du solde
        # ----------------------------------------------------

        if buyer_wallet_locked.balance < amount:
            raise WenzePaymentError(
                "Solde insuffisant pour payer cette commande."
            )

        # ----------------------------------------------------
        # Commission WENZE
        # Règle officielle : 0 %
        # ----------------------------------------------------

        fee_result = calculate_fee(
            amount=amount,
            fee_type="WENZE",
        )

        fee_amount = Decimal(str(fee_result["fee_amount"]))
        net_amount = Decimal(str(fee_result["net_amount"]))

        if fee_amount != Decimal("0.00"):
            raise WenzePaymentError(
                "La commission WENZE doit être exactement de 0 %."
            )

        if net_amount != amount:
            raise WenzePaymentError(
                "Le montant net WENZE doit être égal au montant de la commande."
            )

        # ----------------------------------------------------
        # Référence paiement
        # ----------------------------------------------------

        payment_reference = (
            f"WENZE-PAY-{uuid4().hex[:16].upper()}"
        )

        # ----------------------------------------------------
        # Débit acheteur
        # ----------------------------------------------------

        debit_wallet(
            wallet=buyer_wallet_locked,
            amount=amount,
            reference=payment_reference + "-OUT",
        )

        # ----------------------------------------------------
        # Crédit vendeur
        # ----------------------------------------------------

        credit_wallet(
            wallet=seller_wallet,
            amount=net_amount,
            reference=payment_reference + "-IN",
        )

        # ----------------------------------------------------
        # Validation définitive du stock
        # ----------------------------------------------------
        # Cette opération est dans le même transaction.atomic()
        # que le débit et le crédit.
        # En cas d'échec, le paiement et le stock sont rollback.
        # ----------------------------------------------------

        locked_product.stock -= quantity

        locked_product.save(
            update_fields=[
                "stock",
                "updated_at",
            ]
        )

        # ----------------------------------------------------
        # Mise à jour commande
        # ----------------------------------------------------

        locked_order.status = "PAID"
        locked_order.payment_method = "WALLET"
        locked_order.payment_reference = payment_reference
        locked_order.payment_fee = fee_amount
        locked_order.paid_at = timezone.now()

        locked_order.save(
            update_fields=[
                "status",
                "payment_method",
                "payment_reference",
                "payment_fee",
                "paid_at",
                "updated_at",
            ]
        )

        return {
            "success": True,
            "order_id": locked_order.id,
            "order_reference": locked_order.reference,
            "payment_reference": payment_reference,
            "amount": amount,
            "fee_percentage": Decimal("0.000"),
            "fee_amount": fee_amount,
            "net_amount": net_amount,
            "buyer_wallet_id": buyer_wallet_locked.id,
            "seller_wallet_id": seller_wallet.id,
            "currency": locked_order.currency,
            "status": locked_order.status,
            "transaction_created": True,
            "simulation": False,
        }


def payment_method_status(payment_method):
    statuses = {
        "WALLET": {
            "available": True,
            "label": "Portefeuille NSIKAY",
        },
        "MOBILE_MONEY": {
            "available": False,
            "label": "Mobile Money",
            "reason": "Passerelle de paiement externe non connectée.",
        },
        "VISA": {
            "available": False,
            "label": "Carte Visa",
            "reason": "Passerelle de paiement externe non connectée.",
        },
    }

    return statuses.get(
        payment_method,
        {
            "available": False,
            "label": payment_method,
            "reason": "Méthode de paiement inconnue.",
        },
    )
