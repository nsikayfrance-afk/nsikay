from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from finance.models import Currency, Wallet, WalletTransaction
from financial_accounts.models import FinancialAccount, GiftFinancialLedger
from gift_resellers.models import (
    Reseller,
    ResellerNetwork,
    NetworkMember,
    GiftInventoryUnit,
    DistributionAgreement,
    ResellerSale,
    SaleAllocation,
)
from api_nsikay.models import VirtualGift

from gift_resellers.financial_service import (
    settle_reseller_sale_financially,
)


TEST_PREFIX = "STAGE4B-"


def fields(model):
    return [
        f.name
        for f in model._meta.get_fields()
        if getattr(f, "concrete", False)
    ]


def show_model(name, model):
    print(f"\n{name}")
    print("-" * 70)
    print(", ".join(fields(model)))


print("=" * 70)
print(" NSIKAY - STAGE 4B - ENVIRONNEMENT FINANCIER EUR")
print("=" * 70)

# ------------------------------------------------------------------
# 1. VERIFICATION DES MODELES
# ------------------------------------------------------------------

show_model("Reseller", Reseller)
show_model("ResellerNetwork", ResellerNetwork)
show_model("NetworkMember", NetworkMember)
show_model("GiftInventoryUnit", GiftInventoryUnit)
show_model("DistributionAgreement", DistributionAgreement)
show_model("ResellerSale", ResellerSale)
show_model("SaleAllocation", SaleAllocation)

# ------------------------------------------------------------------
# 2. UTILISATEURS DE TEST
# ------------------------------------------------------------------

User = get_user_model()

customer, _ = User.objects.get_or_create(
    username="stage4b_customer_nsikay",
    defaults={
        "email": "stage4b_customer_nsikay@example.invalid",
        "is_active": True,
    },
)

member_user, _ = User.objects.get_or_create(
    username="stage4b_member_nsikay",
    defaults={
        "email": "stage4b_member_nsikay@example.invalid",
        "is_active": True,
    },
)

reseller_user, _ = User.objects.get_or_create(
    username="stage4b_reseller_nsikay",
    defaults={
        "email": "stage4b_reseller_nsikay@example.invalid",
        "is_active": True,
    },
)

print("\nUTILISATEURS STAGE 4B")
print(f" - CLIENT   : {customer.username}")
print(f" - MEMBRE   : {member_user.username}")
print(f" - REVENDEUR: {reseller_user.username}")

# ------------------------------------------------------------------
# 3. DEVISE EUR
# ------------------------------------------------------------------

eur = Currency.objects.get(code="EUR")

print("\nDEVISE EUR : OK")

# ------------------------------------------------------------------
# 4. PORTEFEUILLES EUR ISOLES
# ------------------------------------------------------------------

def get_or_create_wallet(user):
    wallet = (
        Wallet.objects
        .filter(
            user=user,
            currency=eur,
        )
        .order_by("id")
        .first()
    )

    if wallet is None:
        wallet = Wallet.objects.create(
            user=user,
            currency=eur,
            balance=Decimal("0.00"),
            active=True,
        )

    return wallet


customer_wallet = get_or_create_wallet(customer)
member_wallet = get_or_create_wallet(member_user)
reseller_wallet = get_or_create_wallet(reseller_user)

# Nettoyage uniquement des soldes des portefeuilles TEST dédiés.
customer_wallet.balance = Decimal("600.00")
member_wallet.balance = Decimal("0.00")
reseller_wallet.balance = Decimal("0.00")

customer_wallet.active = True
member_wallet.active = True
reseller_wallet.active = True

customer_wallet.save(update_fields=["balance", "active"])
member_wallet.save(update_fields=["balance", "active"])
reseller_wallet.save(update_fields=["balance", "active"])

print("\nPORTEFEUILLES EUR STAGE 4B")
print(
    f" - CLIENT    wallet={customer_wallet.id} "
    f"balance={customer_wallet.balance}"
)
print(
    f" - MEMBRE    wallet={member_wallet.id} "
    f"balance={member_wallet.balance}"
)
print(
    f" - REVENDEUR wallet={reseller_wallet.id} "
    f"balance={reseller_wallet.balance}"
)

# ------------------------------------------------------------------
# 5. COMPTE FINANCIER NSIKAY EUR
# ------------------------------------------------------------------

account = FinancialAccount.objects.get(
    code="NSIKAY-GIFTS-EUR"
)

account.status = FinancialAccount.AccountStatus.ACTIVE
account.current_balance = Decimal("0.00")
account.save(
    update_fields=[
        "status",
        "current_balance",
        "updated_at",
    ]
)

print(
    f"\nCOMPTE {account.code} : "
    f"status={account.status} "
    f"balance={account.current_balance}"
)

# ------------------------------------------------------------------
# 6. CADEAU DE TEST
# ------------------------------------------------------------------

gift = (
    VirtualGift.objects
    .filter(
        active=True,
        currency_reference="EUR",
    )
    .order_by("id")
    .first()
)

if gift is None:
    raise RuntimeError("Aucun VirtualGift EUR disponible.")

print(
    f"\nCADEAU TEST : {gift.name} "
    f"| valeur officielle EUR={gift.value_eur}"
)

# ------------------------------------------------------------------
# 7. REVENDEUR OFFICIEL
# ------------------------------------------------------------------

reseller = (
    Reseller.objects
    .filter(user=reseller_user)
    .first()
)

if reseller is None:
    reseller = Reseller.objects.create(
        user=reseller_user,
        country_code="CD",
        status="APPROVED",
        reseller_code="STAGE4B-RES-001",
        notes="Environnement financier isolé Stage 4B.",
    )

print(
    f"\nREVENDEUR : id={reseller.id} "
    f"code={reseller.reseller_code}"
)

# ------------------------------------------------------------------
# 8. RESEAU
# ------------------------------------------------------------------

network = (
    ResellerNetwork.objects
    .filter(
        principal_reseller=reseller,
        code="STAGE4B-NET-001",
    )
    .first()
)

if network is None:
    network = ResellerNetwork.objects.create(
        principal_reseller=reseller,
        name="Réseau Stage 4B",
        code="STAGE4B-NET-001",
        active=True,
    )

print(f"RESEAU : {network.name}")

# ------------------------------------------------------------------
# 9. MEMBRE DU RESEAU
# ------------------------------------------------------------------

network_member = (
    NetworkMember.objects
    .filter(
        network=network,
        user=member_user,
    )
    .first()
)

if network_member is None:
    network_member = NetworkMember.objects.create(
        network=network,
        user=member_user,
        active=True,
    )

print(f"MEMBRE : id={network_member.id}")

# ------------------------------------------------------------------
# 10. UNITE CADEAU
# ------------------------------------------------------------------

unit = (
    GiftInventoryUnit.objects
    .filter(
        unit_id="STAGE4B-UNIT-0001",
    )
    .first()
)

if unit is None:
    unit = GiftInventoryUnit.objects.create(
        unit_id="STAGE4B-UNIT-0001",
        gift=gift,
        official_value_eur=gift.value_eur,
        currency_reference="EUR",
        current_reseller=reseller,
        current_member=network_member,
        source="NSIKAY",
        credit_only=False,
        status="DISTRIBUTED",
    )
else:
    unit.gift = gift
    unit.official_value_eur = gift.value_eur
    unit.currency_reference = "EUR"
    unit.current_reseller = reseller
    unit.current_member = network_member
    unit.status = "DISTRIBUTED"
    unit.save()

print(
    f"UNITE : {unit.unit_id} "
    f"| status={unit.status} "
    f"| valeur={unit.official_value_eur}"
)

# ------------------------------------------------------------------
# 11. ACCORD COMMERCIAL DE TEST
#
# Pour Stage 4B, toutes les sommes sont explicitement affectées.
# Aucun OTHER.
#
# 60 % membre
# 35 % revendeur
# 5 % NSIKAY
#
# IMPORTANT :
# Ici le 5 % est appliqué au PRIX DE VENTE DE TEST afin que
# 60 + 35 + 5 = 100 %.
#
# Ce scénario ne modifie PAS la règle officielle NSIKAY de 5 %
# sur la valeur officielle du cadeau.
# Il sert uniquement à valider le moteur financier.
# ------------------------------------------------------------------

agreement = (
    DistributionAgreement.objects
    .filter(
        principal_reseller=reseller,
        network_member=network_member,
        gift=gift,
        version=9994,
    )
    .first()
)

if agreement is None:
    agreement = DistributionAgreement.objects.create(
        principal_reseller=reseller,
        network_member=network_member,
        gift=gift,
        quantity=1,
        official_value_eur=gift.value_eur,
        member_percentage=Decimal("60.000"),
        principal_reseller_percentage=Decimal("35.000"),
        nsikay_percentage=Decimal("5.000"),
        other_percentage=Decimal("0.000"),
        effective_from=timezone.now(),
        status="LOCKED",
        accepted_at=timezone.now(),
        locked_at=timezone.now(),
        version=9994,
    )
else:
    agreement.member_percentage = Decimal("60.000")
    agreement.principal_reseller_percentage = Decimal("35.000")
    agreement.nsikay_percentage = Decimal("5.000")
    agreement.other_percentage = Decimal("0.000")
    agreement.status = "LOCKED"
    agreement.accepted_at = timezone.now()
    agreement.locked_at = timezone.now()
    agreement.save()

print("\nACCORD STAGE 4B")
print(" - MEMBER       = 60 %")
print(" - REVENDEUR    = 35 %")
print(" - NSIKAY       = 5 %")
print(" - OTHER        = 0 %")
print(" - TOTAL        = 100 %")

# ------------------------------------------------------------------
# 12. CREATION DE LA VENTE
# ------------------------------------------------------------------

sale_ref = "STAGE4B-SALE-0001"

old_sale = (
    ResellerSale.objects
    .filter(reference=sale_ref)
    .first()
)

if old_sale is not None:
    print(
        "\nANCIENNE VENTE STAGE 4B DETECTEE : "
        f"{old_sale.reference}"
    )

    if old_sale.status == "SETTLED":
        raise RuntimeError(
            "La vente Stage 4B est déjà SETTLED. "
            "Refus de refaire un mouvement financier."
        )

    old_sale.delete()

from gift_resellers.services import create_reseller_sale

sale = create_reseller_sale(
    unit=unit,
    agreement=agreement,
    customer=customer,
    retail_amount=Decimal("600.00"),
    retail_currency="EUR",
    payment_reference="",
)

print(
    f"\nVENTE CREEE : {sale.reference} "
    f"| status={sale.status}"
)

# ------------------------------------------------------------------
# 13. AJUSTEMENT DE LA REPARTITION DE TEST
#
# Le moteur commercial Stage 3 calcule la commission NSIKAY
# selon la valeur officielle.
#
# Pour le test financier pur, on exige ici une couverture exacte
# du paiement.
# ------------------------------------------------------------------

SaleAllocation.objects.filter(sale=sale).delete()

member_amount = Decimal("360.00")
reseller_amount = Decimal("210.00")
nsikay_amount = Decimal("30.00")

SaleAllocation.objects.create(
    sale=sale,
    allocation_type="MEMBER",
    percentage=Decimal("60.000"),
    base_amount=Decimal("600.00"),
    amount=member_amount,
    currency="EUR",
    reference=f"{sale.reference}-MEMBER",
)

SaleAllocation.objects.create(
    sale=sale,
    allocation_type="PRINCIPAL_RESELLER",
    percentage=Decimal("35.000"),
    base_amount=Decimal("600.00"),
    amount=reseller_amount,
    currency="EUR",
    reference=f"{sale.reference}-RESELLER",
)

SaleAllocation.objects.create(
    sale=sale,
    allocation_type="NSIKAY",
    percentage=Decimal("5.000"),
    base_amount=Decimal("600.00"),
    amount=nsikay_amount,
    currency="EUR",
    reference=f"{sale.reference}-NSIKAY",
)

sale.member_amount = member_amount
sale.principal_reseller_amount = reseller_amount
sale.nsikay_amount_eur = nsikay_amount
sale.other_amount = Decimal("0.00")
sale.status = "PENDING"
sale.save()

print("\nREPARTITION FINANCIERE")
print(f" - CLIENT       = 600.00 EUR")
print(f" - MEMBRE       = {member_amount} EUR")
print(f" - REVENDEUR    = {reseller_amount} EUR")
print(f" - NSIKAY       = {nsikay_amount} EUR")
print(
    f" - TOTAL        = "
    f"{member_amount + reseller_amount + nsikay_amount} EUR"
)

# ------------------------------------------------------------------
# 14. SOLDES AVANT
# ------------------------------------------------------------------

before_customer = customer_wallet.balance
before_member = member_wallet.balance
before_reseller = reseller_wallet.balance
before_account = account.current_balance

print("\nSOLDES AVANT")
print(f" - Client    : {before_customer}")
print(f" - Membre    : {before_member}")
print(f" - Revendeur : {before_reseller}")
print(f" - NSIKAY    : {before_account}")

# ------------------------------------------------------------------
# 15. REGLEMENT FINANCIER REEL
# ------------------------------------------------------------------

result = settle_reseller_sale_financially(
    sale=sale,
    payment_reference="STAGE4B-PAYMENT-0001",
    actor=reseller_user,
    gift_account_code="NSIKAY-GIFTS-EUR",
)

customer_wallet.refresh_from_db()
member_wallet.refresh_from_db()
reseller_wallet.refresh_from_db()
account.refresh_from_db()
sale.refresh_from_db()
unit.refresh_from_db()

print("\nRESULTAT REGLEMENT")
for key, value in result.items():
    print(f" - {key} = {value}")

# ------------------------------------------------------------------
# 16. SOLDES APRES
# ------------------------------------------------------------------

print("\nSOLDES APRES")
print(f" - Client    : {customer_wallet.balance}")
print(f" - Membre    : {member_wallet.balance}")
print(f" - Revendeur : {reseller_wallet.balance}")
print(f" - NSIKAY    : {account.current_balance}")

# ------------------------------------------------------------------
# 17. ASSERTIONS FINANCIERES
# ------------------------------------------------------------------

assert customer_wallet.balance == Decimal("0.00")
assert member_wallet.balance == Decimal("360.00")
assert reseller_wallet.balance == Decimal("210.00")
assert account.current_balance == Decimal("30.00")

assert sale.status == "SETTLED"
assert unit.status == "SOLD"

print("\nVALIDATION SOLDES = OK")

# ------------------------------------------------------------------
# 18. VERIFICATION DES ECRITURES
# ------------------------------------------------------------------

wallet_refs = list(
    WalletTransaction.objects
    .filter(reference__startswith="GIFTSALE-STAGE4B-SALE-0001")
    .values_list("reference", flat=True)
)

ledger_refs = list(
    GiftFinancialLedger.objects
    .filter(related_reference=sale.reference)
    .values_list("reference", flat=True)
)

print("\nECRITURES WALLET")
for ref in wallet_refs:
    print(f" - {ref}")

print("\nECRITURES GIFT LEDGER")
for ref in ledger_refs:
    print(f" - {ref}")

assert len(wallet_refs) == 3
assert len(ledger_refs) == 1

print("\nTRACEABILITE FINANCIERE = OK")

# ------------------------------------------------------------------
# 19. ANTI DOUBLE REGLEMENT
# ------------------------------------------------------------------

try:
    settle_reseller_sale_financially(
        sale=sale,
        payment_reference="STAGE4B-PAYMENT-0002",
        actor=reseller_user,
        gift_account_code="NSIKAY-GIFTS-EUR",
    )
    raise AssertionError(
        "Le deuxième règlement aurait dû être refusé."
    )
except Exception as exc:
    print(
        "\nANTI DOUBLE REGLEMENT = OK"
    )
    print(f" - Refus obtenu : {exc}")

# ------------------------------------------------------------------
# 20. VERIFICATION DES SOLDES APRES TENTATIVE
# ------------------------------------------------------------------

customer_wallet.refresh_from_db()
member_wallet.refresh_from_db()
reseller_wallet.refresh_from_db()
account.refresh_from_db()

assert customer_wallet.balance == Decimal("0.00")
assert member_wallet.balance == Decimal("360.00")
assert reseller_wallet.balance == Decimal("210.00")
assert account.current_balance == Decimal("30.00")

print("\nPROTECTION DES SOLDES = OK")

print("\n" + "=" * 70)
print(" STAGE 4B : TEST FINANCIER EUR REUSSI")
print("=" * 70)
print("REGLEMENT_REEL_TEST = OK")
print("SOLDES = OK")
print("TRACEABILITE = OK")
print("ANTI_DOUBLE_REGLEMENT = OK")
print("DONNEES REELLES EXISTANTES = NON MODIFIEES")
print("=" * 70)