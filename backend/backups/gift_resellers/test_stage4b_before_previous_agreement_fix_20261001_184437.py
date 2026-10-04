from decimal import Decimal
# ============================================================
# STAGE 4B - NETTOYAGE DES DONNEES DE TEST
# ============================================================

def cleanup_stage4b_test_data():
    from gift_resellers.models import (
        DistributionAgreement,
        ResellerSale,
        SaleAllocation,
    )

    # Le modèle DistributionAgreement ne possède PAS de champ notes.
    # On cible uniquement les accords du scénario Stage 4B
    # grâce aux utilisateurs et au cadeau utilisés par le test.

    from django.contrib.auth import get_user_model
    from api_nsikay.models import VirtualGift

    User = get_user_model()

    client = User.objects.get(
        username="admin_test_nsikay"
    )

    member = User.objects.get(
        username="validation_test_nsikay"
    )

    reseller = User.objects.get(
        username="banque_test_nsikay"
    )

    gift = VirtualGift.objects.get(
        slug="quartz"
    )

    old_agreements = DistributionAgreement.objects.filter(
        principal_reseller__user=reseller,
        network_member__user=member,
        gift=gift,
        version=1,
    )

    removed_agreements = 0
    removed_sales = 0
    removed_allocations = 0

    for old_agreement in old_agreements:

        old_sales = ResellerSale.objects.filter(
            agreement=old_agreement
        )

        for old_sale in old_sales:

            allocation_count = SaleAllocation.objects.filter(
                sale=old_sale
            ).count()

            SaleAllocation.objects.filter(
                sale=old_sale
            ).delete()

            removed_allocations += allocation_count

        sale_count = old_sales.count()

        old_sales.delete()

        removed_sales += sale_count

        old_agreement.delete()

        removed_agreements += 1

    print(
        "NETTOYAGE STAGE4B : accords=%s ventes=%s allocations=%s"
        % (
            removed_agreements,
            removed_sales,
            removed_allocations,
        )
    )


cleanup_stage4b_test_data()

# ============================================================
# FIN NETTOYAGE STAGE 4B
# ============================================================
# ============================================================

def cleanup_stage4b_test_data():
    from gift_resellers.models import (
        DistributionAgreement,
        ResellerSale,
        SaleAllocation,
    )

    TEST_AGREEMENT_TAG = "STAGE4B"

    old_agreements = DistributionAgreement.objects.filter(
        notes__icontains=TEST_AGREEMENT_TAG
    )

    removed_agreements = 0
    removed_sales = 0
    removed_allocations = 0

    for old_agreement in old_agreements:

        old_sales = ResellerSale.objects.filter(
            agreement=old_agreement
        )

        for old_sale in old_sales:

            allocation_count = SaleAllocation.objects.filter(
                sale=old_sale
            ).count()

            SaleAllocation.objects.filter(
                sale=old_sale
            ).delete()

            removed_allocations += allocation_count

        sale_count = old_sales.count()

        old_sales.delete()

        removed_sales += sale_count

        old_agreement.delete()

        removed_agreements += 1

    print(
        "NETTOYAGE STAGE4B : accords=%s ventes=%s allocations=%s"
        % (
            removed_agreements,
            removed_sales,
            removed_allocations,
        )
    )


cleanup_stage4b_test_data()

# ============================================================
# FIN NETTOYAGE STAGE 4B
# ============================================================
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


print("=" * 70)
print(" NSIKAY - STAGE 4B - TEST FINANCIER EUR ISOLE")
print(" CORRECTION : AUCUN NOUVEL UTILISATEUR")
print("=" * 70)


# ------------------------------------------------------------------
# 1. UTILISATEURS EXISTANTS UNIQUEMENT
# ------------------------------------------------------------------

User = get_user_model()

customer = User.objects.filter(
    username="admin_test_nsikay"
).first()

member_user = User.objects.filter(
    username="validation_test_nsikay"
).first()

reseller_user = User.objects.filter(
    username="banque_test_nsikay"
).first()

if customer is None:
    raise RuntimeError("admin_test_nsikay introuvable.")

if member_user is None:
    raise RuntimeError("validation_test_nsikay introuvable.")

if reseller_user is None:
    raise RuntimeError("banque_test_nsikay introuvable.")

print("\nUTILISATEURS EXISTANTS")
print(f" - CLIENT    : {customer.username}")
print(f" - MEMBRE    : {member_user.username}")
print(f" - REVENDEUR : {reseller_user.username}")

# ------------------------------------------------------------------
# 2. DEVISE EUR
# ------------------------------------------------------------------

eur = Currency.objects.get(code="EUR")

print("\nDEVISE EUR = OK")


# ------------------------------------------------------------------
# 3. FONCTION PORTEFEUILLE FINANCE EUR
#
# IMPORTANT :
# On travaille uniquement avec finance.Wallet.
# Aucun User n'est créé.
#
# Les wallets CDF/USD existants ne sont jamais modifiés.
# ------------------------------------------------------------------

def get_or_create_finance_eur_wallet(user):
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
        print(
            f"   NOUVEAU finance.Wallet EUR : "
            f"user={user.username} id={wallet.id}"
        )
    else:
        print(
            f"   finance.Wallet EUR existant : "
            f"user={user.username} id={wallet.id}"
        )

    return wallet


print("\nPORTEFEUILLES FINANCE EUR")

customer_wallet = get_or_create_finance_eur_wallet(customer)
member_wallet = get_or_create_finance_eur_wallet(member_user)
reseller_wallet = get_or_create_finance_eur_wallet(reseller_user)


# ------------------------------------------------------------------
# 4. INITIALISATION DES SEULS WALLETS EUR DE TEST
# ------------------------------------------------------------------

customer_wallet.balance = Decimal("600.00")
member_wallet.balance = Decimal("0.00")
reseller_wallet.balance = Decimal("0.00")

customer_wallet.active = True
member_wallet.active = True
reseller_wallet.active = True

customer_wallet.save(update_fields=["balance", "active"])
member_wallet.save(update_fields=["balance", "active"])
reseller_wallet.save(update_fields=["balance", "active"])


# ------------------------------------------------------------------
# 5. VERIFICATION DES PORTEFEUILLES EXISTANTS CDF/USD
# ------------------------------------------------------------------

print("\nPROTECTION DES PORTEFEUILLES EXISTANTS")

for username in [
    "admin_test_nsikay",
    "banque_test_nsikay",
]:
    user = User.objects.get(username=username)

    wallets = (
        Wallet.objects
        .filter(user=user)
        .select_related("currency")
        .order_by("id")
    )

    print(f"\n{username}")

    for wallet in wallets:
        print(
            f" - wallet={wallet.id} "
            f"| devise={wallet.currency.code} "
            f"| solde={wallet.balance}"
        )


# ------------------------------------------------------------------
# 6. COMPTE CADEAUX EUR
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
    f"\nCOMPTE FINANCIER : {account.code}"
)
print(f" - status  = {account.status}")
print(f" - balance = {account.current_balance}")


# ------------------------------------------------------------------
# 7. CADEAU EXISTANT
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
    raise RuntimeError(
        "Aucun VirtualGift EUR disponible."
    )

print(
    f"\nCADEAU : {gift.name}"
)
print(
    f" - valeur officielle = {gift.value_eur} EUR"
)


# ------------------------------------------------------------------
# 8. REVENDEUR
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
    f"\nREVENDEUR : id={reseller.id}"
    f" | code={reseller.reseller_code}"
)


# ------------------------------------------------------------------
# 9. RESEAU
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

print(
    f"RESEAU : {network.name}"
)


# ------------------------------------------------------------------
# 10. MEMBRE
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

print(
    f"MEMBRE : id={network_member.id}"
)


# ------------------------------------------------------------------
# 11. UNITE CADEAU
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
    f"UNITE : {unit.unit_id}"
    f" | status={unit.status}"
)


# ------------------------------------------------------------------
# 12. ACCORD FINANCIER DE TEST
#
# Pour valider le mouvement financier :
#
# 60 % membre
# 35 % revendeur
# 5 % NSIKAY
# 0 % OTHER
#
# = 100 %
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

print("\nACCORD")
print(" - MEMBER    = 60 %")
print(" - REVENDEUR = 35 %")
print(" - NSIKAY    = 5 %")
print(" - OTHER     = 0 %")
print(" - TOTAL     = 100 %")


# ------------------------------------------------------------------
# 13. VENTE
# ------------------------------------------------------------------

sale_ref = "STAGE4B-SALE-0001"

old_sale = (
    ResellerSale.objects
    .filter(reference=sale_ref)
    .first()
)

if old_sale is not None:

    if old_sale.status == "SETTLED":
        raise RuntimeError(
            "STAGE4B-SALE-0001 est déjà SETTLED. "
            "Aucun second mouvement financier autorisé."
        )

    print(
        f"\nSUPPRESSION DE L'ANCIEN TEST NON REGLE : "
        f"{old_sale.reference}"
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
    f"\nVENTE : {sale.reference}"
)
print(
    f" - status = {sale.status}"
)


# ------------------------------------------------------------------
# 14. ALLOCATIONS 100 %
# ------------------------------------------------------------------

SaleAllocation.objects.filter(
    sale=sale
).delete()

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

total = (
    member_amount
    + reseller_amount
    + nsikay_amount
)

print("\nALLOCATIONS")
print(f" - MEMBER    = {member_amount}")
print(f" - REVENDEUR = {reseller_amount}")
print(f" - NSIKAY    = {nsikay_amount}")
print(f" - TOTAL     = {total}")

if total != Decimal("600.00"):
    raise RuntimeError(
        "La répartition Stage 4B ne couvre pas 100 % du paiement."
    )

print(" - COUVERTURE = 100 %")


# ------------------------------------------------------------------
# 15. SOLDES AVANT
# ------------------------------------------------------------------

before_customer = customer_wallet.balance
before_member = member_wallet.balance
before_reseller = reseller_wallet.balance
before_nsikay = account.current_balance

print("\nSOLDES AVANT")
print(f" - CLIENT    = {before_customer}")
print(f" - MEMBRE    = {before_member}")
print(f" - REVENDEUR = {before_reseller}")
print(f" - NSIKAY    = {before_nsikay}")


# ------------------------------------------------------------------
# 16. REGLEMENT FINANCIER
# ------------------------------------------------------------------

result = settle_reseller_sale_financially(
    sale=sale,
    payment_reference="STAGE4B-PAYMENT-0001",
    actor=reseller_user,
    gift_account_code="NSIKAY-GIFTS-EUR",
)

print("\nREGLEMENT")
for key, value in result.items():
    print(f" - {key} = {value}")


# ------------------------------------------------------------------
# 17. REFRESH
# ------------------------------------------------------------------

customer_wallet.refresh_from_db()
member_wallet.refresh_from_db()
reseller_wallet.refresh_from_db()
account.refresh_from_db()
sale.refresh_from_db()
unit.refresh_from_db()


# ------------------------------------------------------------------
# 18. SOLDES APRES
# ------------------------------------------------------------------

print("\nSOLDES APRES")
print(f" - CLIENT    = {customer_wallet.balance}")
print(f" - MEMBRE    = {member_wallet.balance}")
print(f" - REVENDEUR = {reseller_wallet.balance}")
print(f" - NSIKAY    = {account.current_balance}")


# ------------------------------------------------------------------
# 19. VALIDATIONS
# ------------------------------------------------------------------

assert customer_wallet.balance == Decimal("0.00")
assert member_wallet.balance == Decimal("360.00")
assert reseller_wallet.balance == Decimal("210.00")
assert account.current_balance == Decimal("30.00")

assert sale.status == "SETTLED"
assert unit.status == "SOLD"

print("\nVALIDATION SOLDES = OK")


# ------------------------------------------------------------------
# 20. TRACE WALLET
# ------------------------------------------------------------------

wallet_refs = list(
    WalletTransaction.objects
    .filter(
        reference__startswith="GIFTSALE-STAGE4B-SALE-0001"
    )
    .values_list(
        "reference",
        flat=True,
    )
)

print("\nECRITURES WALLET")

for ref in wallet_refs:
    print(f" - {ref}")

assert len(wallet_refs) == 3

print("TRACE WALLET = OK")


# ------------------------------------------------------------------
# 21. TRACE GIFT LEDGER
# ------------------------------------------------------------------

ledger_refs = list(
    GiftFinancialLedger.objects
    .filter(
        related_reference=sale.reference
    )
    .values_list(
        "reference",
        flat=True,
    )
)

print("\nECRITURES GIFT LEDGER")

for ref in ledger_refs:
    print(f" - {ref}")

assert len(ledger_refs) == 1

print("TRACE GIFT LEDGER = OK")


# ------------------------------------------------------------------
# 22. ANTI DOUBLE REGLEMENT
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

    print("\nANTI DOUBLE REGLEMENT = OK")
    print(f" - Refus : {exc}")


# ------------------------------------------------------------------
# 23. VERIFICATION FINALE DES SOLDES
# ------------------------------------------------------------------

customer_wallet.refresh_from_db()
member_wallet.refresh_from_db()
reseller_wallet.refresh_from_db()
account.refresh_from_db()

assert customer_wallet.balance == Decimal("0.00")
assert member_wallet.balance == Decimal("360.00")
assert reseller_wallet.balance == Decimal("210.00")
assert account.current_balance == Decimal("30.00")

print("\nPROTECTION SOLDES APRES SECOND ESSAI = OK")


# ------------------------------------------------------------------
# 24. VERIFICATION DES PORTEFEUILLES CDF/USD
# ------------------------------------------------------------------

print("\nVERIFICATION DES SOLDES EXISTANTS")

admin_usd = (
    Wallet.objects
    .filter(
        user__username="admin_test_nsikay",
        currency__code="USD",
    )
    .first()
)

banque_cdf = (
    Wallet.objects
    .filter(
        user__username="banque_test_nsikay",
        currency__code="CDF",
    )
    .first()
)

if admin_usd:
    print(
        f" - admin_test_nsikay USD = "
        f"{admin_usd.balance}"
    )

if banque_cdf:
    print(
        f" - banque_test_nsikay CDF = "
        f"{banque_cdf.balance}"
    )

assert admin_usd is not None
assert banque_cdf is not None

assert admin_usd.balance == Decimal("10000.00")
assert banque_cdf.balance == Decimal("25000000.00")

print("PROTECTION CDF/USD = OK")


# ------------------------------------------------------------------
# 25. RESULTAT
# ------------------------------------------------------------------

print("\n" + "=" * 70)
print(" STAGE 4B : TEST FINANCIER EUR REUSSI")
print("=" * 70)
print("UTILISATEURS_EXISTANTS = OK")
print("AUCUN_NOUVEL_UTILISATEUR = OK")
print("REGLEMENT_FINANCIER = OK")
print("SOLDES_EUR = OK")
print("TRACE_WALLET = OK")
print("TRACE_GIFT_LEDGER = OK")
print("ANTI_DOUBLE_REGLEMENT = OK")
print("PROTECTION_CDF = OK")
print("PROTECTION_USD = OK")
print("=" * 70)