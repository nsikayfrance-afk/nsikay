from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction

from finance.models import Wallet
from wenze.models import WenzeProduct, WenzeOrder
from wenze.payment import WenzePaymentError, pay_wenze_order_with_wallet


User = get_user_model()

print("")
print("=" * 70)
print(" NSIKAY - TESTS ERREURS PAIEMENT WENZE")
print("=" * 70)

buyer = User.objects.get(username="admin_test_nsikay")
seller = User.objects.get(username="finance_test_nsikay")

buyer_wallet = Wallet.objects.get(
    user=buyer,
    active=True,
    currency__code="USD",
)

seller_wallet = Wallet.objects.get(
    user=seller,
    active=True,
)

print(f"ACHETEUR : {buyer.username}")
print(f"VENDEUR  : {seller.username}")
print(f"PORTEFEUILLE ACHETEUR : #{buyer_wallet.id} / {buyer_wallet.currency.code}")
print(f"PORTEFEUILLE VENDEUR  : #{seller_wallet.id} / {seller_wallet.currency.code}")

# ============================================================
# TEST 1 - SOLDE INSUFFISANT
# ============================================================

print("")
print("-" * 70)
print("TEST 1 - SOLDE INSUFFISANT")
print("-" * 70)

try:
    with transaction.atomic():
        original_buyer_currency = buyer_wallet.currency
        original_buyer_balance = buyer_wallet.balance
        original_seller_currency = seller_wallet.currency
        original_seller_balance = seller_wallet.balance

        seller_wallet.currency = buyer_wallet.currency
        seller_wallet.balance = Decimal("0.00")
        seller_wallet.save(update_fields=["currency", "balance"])

        buyer_wallet.balance = Decimal("10.00")
        buyer_wallet.save(update_fields=["balance"])

        product = WenzeProduct.objects.create(
            seller=seller,
            name="TEST ERREUR SOLDE",
            description="Produit temporaire de test",
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
            reference="TEST-INSUFFISANT",
        )

        try:
            pay_wenze_order_with_wallet(
                order=order,
                buyer_wallet=buyer_wallet,
            )
            print("ERREUR : le paiement aurait dû être refusé.")
        except WenzePaymentError as exc:
            print(f"REFUS CORRECT : {exc}")

        order.refresh_from_db()

        if order.status == "PENDING":
            print("Statut commande : PENDING -> OK")
        else:
            print(f"ERREUR : statut inattendu = {order.status}")

        if buyer_wallet.balance == Decimal("10.00"):
            print("Solde acheteur inchangé -> OK")
        else:
            print(f"ERREUR : solde acheteur = {buyer_wallet.balance}")

        raise RuntimeError("ROLLBACK_TEST")

except RuntimeError as exc:
    if str(exc) == "ROLLBACK_TEST":
        print("Rollback TEST 1 : OK")
    else:
        raise


# ============================================================
# TEST 2 - MAUVAISE DEVISE
# ============================================================

print("")
print("-" * 70)
print("TEST 2 - MAUVAISE DEVISE DU PORTEFEUILLE")
print("-" * 70)

try:
    with transaction.atomic():
        original_buyer_currency = buyer_wallet.currency
        original_buyer_balance = buyer_wallet.balance
        original_seller_currency = seller_wallet.currency
        original_seller_balance = seller_wallet.balance

        seller_wallet.currency = buyer_wallet.currency
        seller_wallet.balance = Decimal("1000.00")
        seller_wallet.save(update_fields=["currency", "balance"])

        # On force temporairement le portefeuille acheteur en EUR.
        eur_wallet = Wallet.objects.filter(
            user=buyer,
            active=True,
            currency__code="EUR",
        ).first()

        if eur_wallet is None:
            print("Aucun portefeuille EUR disponible pour ce test.")
            raise RuntimeError("ROLLBACK_TEST")

        eur_original_balance = eur_wallet.balance
        eur_wallet.balance = Decimal("1000.00")
        eur_wallet.save(update_fields=["balance"])

        product = WenzeProduct.objects.create(
            seller=seller,
            name="TEST ERREUR DEVISE",
            description="Produit temporaire de test",
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
            reference="TEST-DEVISE",
        )

        try:
            pay_wenze_order_with_wallet(
                order=order,
                buyer_wallet=eur_wallet,
            )
            print("ERREUR : la mauvaise devise aurait dû être refusée.")
        except WenzePaymentError as exc:
            print(f"REFUS CORRECT : {exc}")

        order.refresh_from_db()

        if order.status == "PENDING":
            print("Statut commande : PENDING -> OK")
        else:
            print(f"ERREUR : statut inattendu = {order.status}")

        if eur_wallet.balance == Decimal("1000.00"):
            print("Solde portefeuille EUR inchangé -> OK")
        else:
            print(f"ERREUR : solde EUR = {eur_wallet.balance}")

        raise RuntimeError("ROLLBACK_TEST")

except RuntimeError as exc:
    if str(exc) == "ROLLBACK_TEST":
        print("Rollback TEST 2 : OK")
    else:
        raise


# ============================================================
# TEST 3 - VENDEUR SANS PORTEFEUILLE COMPATIBLE
# ============================================================

print("")
print("-" * 70)
print("TEST 3 - VENDEUR SANS PORTEFEUILLE COMPATIBLE")
print("-" * 70)

try:
    with transaction.atomic():
        original_buyer_currency = buyer_wallet.currency
        original_buyer_balance = buyer_wallet.balance
        original_seller_currency = seller_wallet.currency
        original_seller_balance = seller_wallet.balance

        buyer_wallet.balance = Decimal("1000.00")
        buyer_wallet.save(update_fields=["balance"])

        # Le portefeuille vendeur est volontairement mis en EUR.
        seller_wallet.currency = original_buyer_currency
        seller_wallet.balance = Decimal("500.00")
        seller_wallet.save(update_fields=["currency", "balance"])

        # Désactivation temporaire de tous les wallets USD du vendeur.
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
            name="TEST VENDEUR SANS WALLET",
            description="Produit temporaire de test",
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
            reference="TEST-SELLER-WALLET",
        )

        try:
            pay_wenze_order_with_wallet(
                order=order,
                buyer_wallet=buyer_wallet,
            )
            print("ERREUR : le paiement aurait dû être refusé.")
        except WenzePaymentError as exc:
            print(f"REFUS CORRECT : {exc}")

        order.refresh_from_db()

        if order.status == "PENDING":
            print("Statut commande : PENDING -> OK")
        else:
            print(f"ERREUR : statut inattendu = {order.status}")

        if buyer_wallet.balance == Decimal("1000.00"):
            print("Aucun débit acheteur -> OK")
        else:
            print(f"ERREUR : solde acheteur = {buyer_wallet.balance}")

        raise RuntimeError("ROLLBACK_TEST")

except RuntimeError as exc:
    if str(exc) == "ROLLBACK_TEST":
        print("Rollback TEST 3 : OK")
    else:
        raise


# ============================================================
# VERIFICATION FINALE
# ============================================================

print("")
print("-" * 70)
print("VERIFICATION FINALE")
print("-" * 70)

print(f"Produits WENZE : {WenzeProduct.objects.count()}")
print(f"Commandes WENZE : {WenzeOrder.objects.count()}")

print("")
print("TESTS ERREURS PAIEMENT WENZE : TERMINE")
print("=" * 70)