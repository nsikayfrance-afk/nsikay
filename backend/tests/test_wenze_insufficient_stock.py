from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction

from finance.models import Wallet, WalletTransaction
from wenze.models import WenzeProduct, WenzeOrder
from wenze.payment import pay_wenze_order_with_wallet, WenzePaymentError


User = get_user_model()

print("")
print("=" * 70)
print(" TEST WENZE - STOCK INSUFFISANT AU PAIEMENT")
print("=" * 70)

buyer = User.objects.get(
    username="admin_test_nsikay"
)

seller = User.objects.get(
    username="finance_test_nsikay"
)

buyer_wallet = Wallet.objects.get(
    user=buyer,
    active=True,
    currency__code="USD",
)

seller_wallet = Wallet.objects.filter(
    user=seller,
    active=True,
).first()

if seller_wallet is None:
    raise RuntimeError(
        "Aucun portefeuille actif vendeur disponible."
    )

print("")
print("Acheteur :", buyer.username)
print("Wallet acheteur :", buyer_wallet.id, buyer_wallet.currency.code)
print("Vendeur :", seller.username)
print("Wallet vendeur :", seller_wallet.id, seller_wallet.currency.code)

try:

    with transaction.atomic():

        original_buyer_balance = buyer_wallet.balance
        original_seller_balance = seller_wallet.balance
        original_seller_currency = seller_wallet.currency

        seller_wallet.currency = buyer_wallet.currency
        seller_wallet.balance = Decimal("100.00")
        seller_wallet.save(
            update_fields=[
                "currency",
                "balance",
            ]
        )

        buyer_wallet.balance = Decimal("1000.00")
        buyer_wallet.save(
            update_fields=["balance"]
        )

        # ----------------------------------------------------
        # Produit avec seulement 1 unité disponible
        # ----------------------------------------------------

        product = WenzeProduct.objects.create(
            seller=seller,
            name="TEST STOCK INSUFFISANT",
            description="Produit temporaire pour test de sécurité stock",
            price=Decimal("200.00"),
            currency="USD",
            stock=1,
            status="ACTIVE",
        )

        print("")
        print("Stock initial :", product.stock)

        # ----------------------------------------------------
        # Commande de 2 unités
        # ----------------------------------------------------

        order = WenzeOrder.objects.create(
            buyer=buyer,
            product=product,
            quantity=2,
            unit_price=Decimal("200.00"),
            currency="USD",
            total_amount=Decimal("400.00"),
            reference="TEST-STOCK-INSUFFICIENT",
        )

        product.refresh_from_db()

        print(
            "Stock après création commande :",
            product.stock,
        )

        if product.stock == 1:
            print(
                "Stock non consommé avant paiement : OK"
            )
        else:
            print(
                "ERREUR stock avant paiement :",
                product.stock,
            )

        buyer_before = buyer_wallet.balance
        seller_before = seller_wallet.balance

        # ----------------------------------------------------
        # Paiement : doit être refusé
        # ----------------------------------------------------

        payment_refused = False

        try:

            pay_wenze_order_with_wallet(
                order=order,
                buyer_wallet=buyer_wallet,
            )

        except WenzePaymentError as exc:

            payment_refused = True

            print("")
            print(
                "Paiement refusé correctement :",
                str(exc),
            )

        # ----------------------------------------------------
        # Vérifications après refus
        # ----------------------------------------------------

        product.refresh_from_db()
        order.refresh_from_db()
        buyer_wallet.refresh_from_db()
        seller_wallet.refresh_from_db()

        print("")
        print("Statut commande :", order.status)
        print("Stock final :", product.stock)
        print("Solde acheteur :", buyer_wallet.balance)
        print("Solde vendeur :", seller_wallet.balance)

        if payment_refused:
            print(
                "Refus du paiement pour stock insuffisant : OK"
            )
        else:
            print(
                "ERREUR : paiement accepté malgré stock insuffisant."
            )

        if order.status == "PENDING":
            print(
                "Commande reste PENDING : OK"
            )
        else:
            print(
                "ERREUR statut commande :",
                order.status,
            )

        if product.stock == 1:
            print(
                "Stock reste à 1 : OK"
            )
        else:
            print(
                "ERREUR stock final :",
                product.stock,
            )

        if buyer_wallet.balance == buyer_before:
            print(
                "Aucun débit acheteur : OK"
            )
        else:
            print(
                "ERREUR débit acheteur :",
                buyer_wallet.balance,
            )

        if seller_wallet.balance == seller_before:
            print(
                "Aucun crédit vendeur : OK"
            )
        else:
            print(
                "ERREUR crédit vendeur :",
                seller_wallet.balance,
            )

        # ----------------------------------------------------
        # Vérification des écritures financières
        # ----------------------------------------------------

        out_count = WalletTransaction.objects.filter(
            wallet=buyer_wallet,
            transaction_type="withdraw",
            reference__startswith="WENZE-PAY-",
        ).count()

        in_count = WalletTransaction.objects.filter(
            wallet=seller_wallet,
            transaction_type="deposit",
            reference__startswith="WENZE-PAY-",
        ).count()

        print("")
        print(
            "WalletTransaction OUT :",
            out_count,
        )

        print(
            "WalletTransaction IN :",
            in_count,
        )

        if out_count == 0:
            print(
                "Aucune écriture débit : OK"
            )
        else:
            print(
                "ERREUR : écriture débit détectée."
            )

        if in_count == 0:
            print(
                "Aucune écriture crédit : OK"
            )
        else:
            print(
                "ERREUR : écriture crédit détectée."
            )

        # ----------------------------------------------------
        # Rollback volontaire
        # ----------------------------------------------------

        raise RuntimeError(
            "ROLLBACK_STOCK_INSUFFICIENT_TEST"
        )

except RuntimeError as exc:

    if str(exc) == "ROLLBACK_STOCK_INSUFFICIENT_TEST":
        print("")
        print("=" * 70)
        print("ROLLBACK DU TEST : OK")
        print("=" * 70)

# ------------------------------------------------------------
# Vérification finale
# ------------------------------------------------------------

print("")
print("=" * 70)
print(" VERIFICATION APRES ROLLBACK")
print("=" * 70)

print(
    "Produits WENZE :",
    WenzeProduct.objects.count(),
)

print(
    "Commandes WENZE :",
    WenzeOrder.objects.count(),
)

print(
    "WalletTransactions :",
    WalletTransaction.objects.count(),
)

print("")
print("=" * 70)
print(" TEST STOCK INSUFFISANT : TERMINE")
print("=" * 70)