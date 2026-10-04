from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from finance.models import Wallet
from finance.wallet_service import credit_wallet, debit_wallet
from financial_accounts.models import FinancialAccount, GiftFinancialLedger

from .models import ResellerSale, GiftInventoryUnit


ZERO = Decimal("0.00")


def money(value):
    value = Decimal(value)
    return value.quantize(Decimal("0.01"))


def get_user_wallet(user, currency):
    """
    Retourne le portefeuille finance.Wallet actif de l'utilisateur
    dans la devise demandée.

    Pour Stage 4A, aucune conversion automatique n'est effectuée.
    """
    if user is None:
        raise ValueError("Utilisateur financier absent.")

    wallet = (
        Wallet.objects
        .select_for_update()
        .filter(
            user=user,
            currency__code=currency,
            active=True,
        )
        .order_by("id")
        .first()
    )

    if wallet is None:
        raise ValueError(
            f"Aucun portefeuille actif {currency} pour l'utilisateur "
            f"{getattr(user, 'username', user)}."
        )

    return wallet


def get_gift_financial_account(currency, account_code=None):
    """
    Le compte financier NSIKAY doit être explicitement ACTIVE.
    """
    if account_code is None:
        account_code = f"NSIKAY-GIFTS-{currency}"

    account = (
        FinancialAccount.objects
        .select_for_update()
        .filter(
            code=account_code,
            currency=currency,
        )
        .first()
    )

    if account is None:
        raise ValueError(
            f"Compte financier introuvable : {account_code}"
        )

    if account.status != FinancialAccount.AccountStatus.ACTIVE:
        raise ValueError(
            f"Compte financier {account.code} non actif : "
            f"{account.status}"
        )

    return account


def validate_sale_financial_destination(sale):
    """
    Vérifie qu'un règlement réel ne laisse aucun montant sans destination.
    """

    allocations = sale.allocations.all()

    total_allocated = ZERO

    for allocation in allocations:
        total_allocated += money(allocation.amount)

    retail = money(sale.retail_amount)

    if total_allocated != retail:
        raise ValueError(
            "REGLEMENT REFUSE : la répartition financière ne couvre pas "
            f"exactement le prix payé. payé={retail} "
            f"affecté={total_allocated} "
            f"écart={money(retail - total_allocated)}."
        )

    other = allocations.filter(allocation_type="OTHER").first()

    if other is not None and money(other.amount) > ZERO:
        raise ValueError(
            "REGLEMENT REFUSE : une allocation OTHER possède un montant "
            "mais aucun bénéficiaire financier explicite n'est défini."
        )


@transaction.atomic
def settle_reseller_sale_financially(
    *,
    sale,
    payment_reference,
    actor=None,
    gift_account_code=None,
):
    """
    Règlement financier réel d'une vente de cadeau revendeur.

    Cette fonction effectue réellement :
      - débit client ;
      - crédit membre ;
      - crédit revendeur principal ;
      - enregistrement de la part NSIKAY.

    Elle ne fait aucune conversion monétaire automatique.
    """

    if not payment_reference:
        raise ValueError("payment_reference obligatoire.")

    sale = (
        ResellerSale.objects
        .select_for_update()
        .select_related(
            "agreement",
            "gift_unit",
            "network_member__user",
            "principal_reseller__user",
            "customer",
        )
        .get(pk=sale.pk)
    )

    if sale.status == "SETTLED":
        raise ValueError(
            f"Vente déjà réglée : {sale.reference}"
        )

    if sale.status != "PENDING":
        raise ValueError(
            f"Vente non réglable dans son état actuel : {sale.status}"
        )

    if not sale.gift_unit:
        raise ValueError("Unité cadeau absente.")

    if sale.gift_unit.status != GiftInventoryUnit.Status.DISTRIBUTED:
        raise ValueError(
            "L'unité cadeau doit être DISTRIBUTED avant règlement."
        )

    agreement = sale.agreement

    if agreement.status != "LOCKED":
        raise ValueError(
            "L'accord commercial doit être LOCKED."
        )

    if sale.payment_reference:
        raise ValueError(
            "Cette vente possède déjà une référence de paiement."
        )

    retail_currency = sale.retail_currency

    # --------------------------------------------------------
    # IMPORTANT : pas de conversion automatique Stage 4A
    # --------------------------------------------------------

    customer_wallet = get_user_wallet(
        sale.customer,
        retail_currency,
    )

    member_wallet = get_user_wallet(
        sale.network_member.user,
        retail_currency,
    )

    reseller_wallet = get_user_wallet(
        sale.principal_reseller.user,
        retail_currency,
    )

    # --------------------------------------------------------
    # Compte NSIKAY
    # --------------------------------------------------------

    account = get_gift_financial_account(
        retail_currency,
        account_code=gift_account_code,
    )

    # --------------------------------------------------------
    # Vérification des destinations
    # --------------------------------------------------------

    validate_sale_financial_destination(sale)

    allocations = {
        allocation.allocation_type: allocation
        for allocation in sale.allocations.select_for_update().all()
    }

    member_allocation = allocations.get("MEMBER")
    reseller_allocation = allocations.get("PRINCIPAL_RESELLER")
    nsikay_allocation = allocations.get("NSIKAY")

    if member_allocation is None:
        raise ValueError("Allocation MEMBER absente.")

    if reseller_allocation is None:
        raise ValueError(
            "Allocation PRINCIPAL_RESELLER absente."
        )

    if nsikay_allocation is None:
        raise ValueError("Allocation NSIKAY absente.")

    retail_amount = money(sale.retail_amount)

    member_amount = money(member_allocation.amount)
    reseller_amount = money(reseller_allocation.amount)
    nsikay_amount = money(nsikay_allocation.amount)

    if member_amount + reseller_amount + nsikay_amount != retail_amount:
        raise ValueError(
            "Répartition financière invalide : "
            f"MEMBER={member_amount}, "
            f"RESELLER={reseller_amount}, "
            f"NSIKAY={nsikay_amount}, "
            f"TOTAL={money(member_amount + reseller_amount + nsikay_amount)}, "
            f"PRIX={retail_amount}"
        )

    # --------------------------------------------------------
    # Débit client
    # --------------------------------------------------------

    base_ref = f"GIFTSALE-{sale.reference}"

    debit_wallet(
        customer_wallet,
        retail_amount,
        f"{base_ref}-CUSTOMER",
    )

    # --------------------------------------------------------
    # Crédit membre
    # --------------------------------------------------------

    if member_amount > ZERO:
        credit_wallet(
            member_wallet,
            member_amount,
            f"{base_ref}-MEMBER",
        )

    # --------------------------------------------------------
    # Crédit revendeur principal
    # --------------------------------------------------------

    if reseller_amount > ZERO:
        credit_wallet(
            reseller_wallet,
            reseller_amount,
            f"{base_ref}-RESELLER",
        )

    # --------------------------------------------------------
    # Part NSIKAY
    # --------------------------------------------------------

    if nsikay_amount > ZERO:
        account.current_balance += nsikay_amount
        account.save(
            update_fields=[
                "current_balance",
                "updated_at",
            ]
        )

    GiftFinancialLedger.objects.create(
        reference=f"{base_ref}-NSIKAY",
        operation_type="RESELLER_SALE_NSIkAY_SHARE",
        currency=retail_currency,
        amount=nsikay_amount,
        buyer_reference=str(sale.customer_id),
        sender_reference=str(sale.customer_id),
        beneficiary_reference="NSIKAY",
        financial_account=account,
        related_reference=sale.reference,
    )

    # --------------------------------------------------------
    # Finalisation
    # --------------------------------------------------------

    sale.payment_reference = payment_reference
    sale.status = "SETTLED"
    sale.settled_at = timezone.now()
    sale.save(
        update_fields=[
            "payment_reference",
            "status",
            "settled_at",
        ]
    )

    sale.gift_unit.status = GiftInventoryUnit.Status.SOLD
    sale.gift_unit.save(update_fields=["status"])

    return {
        "sale_reference": sale.reference,
        "status": sale.status,
        "currency": retail_currency,
        "retail_amount": retail_amount,
        "member_amount": member_amount,
        "reseller_amount": reseller_amount,
        "nsikay_amount": nsikay_amount,
        "financial_account": account.code,
    }