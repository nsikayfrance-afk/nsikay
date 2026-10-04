from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction

from finance.models import Wallet, WalletTransaction
from wenze.models import WenzeProduct, WenzeOrder
from wenze.payment import WenzePaymentError, pay_wenze_order_with_wallet


User = get_user_model()

print("")
print("=" * 70)
print(" NSIKAY - TESTS DES ERREURS PAIEMENT WENZE")
print("=" * 70)

buyer = User.objects.get(username="admin_test_nsikay")
seller = User.objects.get(username="finance_test_nsikay")

buyer_wallet = Wallet.objects.get(
    user=buyer,
    active=True,
    currency__code="USD",
)

seller_wallet = Wallet.objects.filter(
    user=seller,
    active=True,
).first()

print("")
print("ACHETEUR :", buyer.username)
print("VENDEUR  :", seller.username)
print("WALLET ACHETEUR :", buyer_wallet.id, buyer_wallet.currency.code)
print("WALLET VENDEUR :", seller_wallet.id, seller_wallet.currency.code)

# ============================================================
# TEST 1 : SOLDE INSUFFISANT
# ============================================================

print("")
print("-" * 70)
print("TEST 1 - SOLDE INSUFFISANT")
print("-" * 70)

try:
    with transaction.atomic():

        original_buyer_balance = buyer_wallet.balance
        original_seller_currency = seller_wallet.currency
        original_seller_balance = seller_wallet.balance

        seller_wallet.currency = buyer_wallet.currency
        seller_wallet.balance = Decimal("1000.00")
        seller_wallet.save(update_fields=["currency", "balance"])

        buyer_wallet.balance = Decimal("10.00")
        buyer_wallet.save(update_fields=["balance"])

        product = WenzeProduct.objects.create(
            seller=seller,
            name="TEST SOLDE INSUFFISANT",
            description="Produit temporaire",
            price=Decimal("200.00"),
            currency="USD",
            stock=5,
            status="ACTIVE",
        )

        order = WenzeOrder.objects.create(
            buyer=buyer,
            product=product,
            quantity=1,
            unit_price=Decimal("200.00"),
            currency="USD",
            total_amount=Decimal("200.00"),
            reference="TEST-INSUFFICIENT-FUNDS",
        )

        try:
            pay_wenze_order_with_wallet(
                order=order,
                buyer_wallet=buyer_wallet,
            )

            print("ERREUR : paiement accepté malgré solde insuffisant.")

        except WenzePaymentError as exc:
            print("REFUS CORRECT :", exc)

        order.refresh_from_db()

        if order.status == "PENDING":
            print("Commande reste PENDING : OK")
        else:
            print("ERREUR statut :", order.status)

        if buyer_wallet.balance == Decimal("10.00"):
            print("Aucun débit acheteur : OK")
        else:
            print("ERREUR solde acheteur :", buyer_wallet.balance)

        raise RuntimeError("ROLLBACK_WENZE_TEST")

except RuntimeError as exc:

    if str(exc) == "ROLLBACK_WENZE_TEST":
        print("Rollback TEST 1 : OK")


# ============================================================
# TEST 2 : MAUVAISE DEVISE
# ============================================================

print("")
print("-" * 70)
print("TEST 2 - MAUVAISE DEVISE")
print("-" * 70)

try:
    with transaction.atomic():

        eur_wallet = Wallet.objects.filter(
            user=buyer,
            active=True,
            currency__code="EUR",
        ).first()

        if eur_wallet is None:
            print("ERREUR : aucun portefeuille EUR disponible.")
            raise RuntimeError("ROLLBACK_WENZE_TEST")

        original_eur_balance = eur_wallet.balance

        seller_wallet.currency = buyer_wallet.currency
        seller_wallet.balance = Decimal("1000.00")
        seller_wallet.save(update_fields=["currency", "balance"])

        eur_wallet.balance = Decimal("1000.00")
        eur_wallet.save(update_fields=["balance"])

        product = WenzeProduct.objects.create(
            seller=seller,
            name="TEST MAUVAISE DEVISE",
            description="Produit temporaire",
            price=Decimal("200.00"),
            currency="USD",
            stock=5,
            status="ACTIVE",
        )

        order = WenzeOrder.objects.create(
            buyer=buyer,
            product=product,
            quantity=1,
            unit_price=Decimal("200.00"),
            currency="USD",
            total_amount=Decimal("200.00"),
            reference="TEST-WRONG-CURRENCY",
        )

        try:
            pay_wenze_order_with_wallet(
                order=order,
                buyer_wallet=eur_wallet,
            )

            print("ERREUR : paiement accepté avec mauvaise devise.")

        except WenzePaymentError as exc:
            print("REFUS CORRECT :", exc)

        order.refresh_from_db()

        if order.status == "PENDING":
            print("Commande reste PENDING : OK")
        else:
            print("ERREUR statut :", order.status)

        if eur_wallet.balance == Decimal("1000.00"):
            print("Aucun débit EUR : OK")
        else:
            print("ERREUR solde EUR :", eur_wallet.balance)

        raise RuntimeError("ROLLBACK_WENZE_TEST")

except RuntimeError as exc:

    if str(exc) == "ROLLBACK_WENZE_TEST":
        print("Rollback TEST 2 : OK")


# ============================================================
# TEST 3 : VENDEUR SANS WALLET COMPATIBLE
# ============================================================

print("")
print("-" * 70)
print("TEST 3 - VENDEUR SANS PORTEFEUILLE COMPATIBLE")
print("-" * 70)

try:
    with transaction.atomic():

        buyer_wallet.balance = Decimal("1000.00")
        buyer_wallet.save(update_fields=["balance"])

        # Tous les wallets USD actifs du vendeur sont désactivés
        seller_usd_wallets = list(
            Wallet.objects.filter(
                user=seller,
                active=True,
                currency__code="USD",
            )
        )

        for wallet in seller_usd_wallets:
            wallet.active = False
            wallet.save(update_fields=["active"])

        product = WenzeProduct.objects.create(
            seller=seller,
            name="TEST SANS WALLET VENDEUR",
            description="Produit temporaire",
            price=Decimal("200.00"),
            currency="USD",
            stock=5,
            status="ACTIVE",
        )

        order = WenzeOrder.objects.create(
            buyer=buyer,
            product=product,
            quantity=1,
            unit_price=Decimal("200.00"),
            currency="USD",
            total_amount=Decimal("200.00"),
            reference="TEST-NO-SELLER-WALLET",
        )

        try:
            pay_wenze_order_with_wallet(
                order=order,
                buyer_wallet=buyer_wallet,
            )

            print("ERREUR : paiement accepté sans wallet vendeur compatible.")

        except WenzePaymentError as exc:
            print("REFUS CORRECT :", exc)

        order.refresh_from_db()

        if order.status == "PENDING":
            print("Commande reste PENDING : OK")
        else:
            print("ERREUR statut :", order.status)

        if buyer_wallet.balance == Decimal("1000.00"):
            print("Aucun débit acheteur : OK")
        else:
            print("ERREUR solde acheteur :", buyer_wallet.balance)

        raise RuntimeError("ROLLBACK_WENZE_TEST")

except RuntimeError as exc:

    if str(exc) == "ROLLBACK_WENZE_TEST":
        print("Rollback TEST 3 : OK")


# ============================================================
# VERIFICATION DES DONNEES
# ============================================================

print("")
print("-" * 70)
print("VERIFICATION DES DONNEES APRES ROLLBACK")
print("-" * 70)

print("Produits WENZE :", WenzeProduct.objects.count())
print("Commandes WENZE :", WenzeOrder.objects.count())
print("WalletTransactions :", WalletTransaction.objects.count())

print("")
print("=" * 70)
print(" TESTS ERREURS WENZE : TERMINE")
print("=" * 70)