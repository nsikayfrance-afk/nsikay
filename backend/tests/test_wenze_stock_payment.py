from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction

from finance.models import Wallet, WalletTransaction
from wenze.models import WenzeProduct, WenzeOrder
from wenze.payment import pay_wenze_order_with_wallet


User = get_user_model()

print("")
print("=" * 70)
print(" TEST WENZE - STOCK + PAIEMENT ATOMIQUE")
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

# On utilise le portefeuille actif existant du vendeur.
# Sa devise sera temporairement alignée sur USD pendant
# la transaction de test, puis le rollback restaurera son état.
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

        # ----------------------------------------------------
        # Sauvegarde temporaire des données financières
        # ----------------------------------------------------

        original_buyer_balance = buyer_wallet.balance
        original_seller_balance = seller_wallet.balance
        original_seller_currency = seller_wallet.currency

        # Le test utilise USD.
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
        # Création produit
        # ----------------------------------------------------

        product = WenzeProduct.objects.create(
            seller=seller,
            name="TEST STOCK ATOMIQUE",
            description="Produit temporaire de validation",
            price=Decimal("200.00"),
            currency="USD",
            stock=5,
            status="ACTIVE",
        )

        print("")
        print("Stock initial :", product.stock)

        # ----------------------------------------------------
        # Création commande
        # ----------------------------------------------------

        order = WenzeOrder.objects.create(
            buyer=buyer,
            product=product,
            quantity=2,
            unit_price=Decimal("200.00"),
            currency="USD",
            total_amount=Decimal("400.00"),
            reference="TEST-STOCK-ATOMIC",
        )

        product.refresh_from_db()

        print(
            "Stock après création commande :",
            product.stock,
        )

        if product.stock == 5:
            print(
                "Stock non consommé avant paiement : OK"
            )
        else:
            print(
                "ERREUR stock avant paiement :",
                product.stock,
            )

        # ----------------------------------------------------
        # Paiement
        # ----------------------------------------------------

        result = pay_wenze_order_with_wallet(
            order=order,
            buyer_wallet=buyer_wallet,
        )

        # ----------------------------------------------------
        # Vérifications
        # ----------------------------------------------------

        product.refresh_from_db()
        order.refresh_from_db()
        buyer_wallet.refresh_from_db()
        seller_wallet.refresh_from_db()

        print("")
        print(
            "Paiement réussi :",
            result["success"],
        )

        print(
            "Statut commande :",
            order.status,
        )

        print(
            "Stock après paiement :",
            product.stock,
        )

        print(
            "Solde acheteur :",
            buyer_wallet.balance,
        )

        print(
            "Solde vendeur :",
            seller_wallet.balance,
        )

        if result["success"] is True:
            print("Paiement effectif : OK")
        else:
            print("ERREUR paiement.")

        if order.status == "PAID":
            print("Commande PAID : OK")
        else:
            print(
                "ERREUR statut :",
                order.status,
            )

        if product.stock == 3:
            print(
                "Stock 5 -> 3 après quantité 2 : OK"
            )
        else:
            print(
                "ERREUR stock final :",
                product.stock,
            )

        if buyer_wallet.balance == Decimal("600.00"):
            print(
                "Débit acheteur 400 : OK"
            )
        else:
            print(
                "ERREUR solde acheteur :",
                buyer_wallet.balance,
            )

        if seller_wallet.balance == Decimal("500.00"):
            print(
                "Crédit vendeur 400 : OK"
            )
        else:
            print(
                "ERREUR solde vendeur :",
                seller_wallet.balance,
            )

        # ----------------------------------------------------
        # Vérification des écritures
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

        if out_count >= 1:
            print(
                "Écriture débit acheteur : OK"
            )
        else:
            print(
                "ERREUR écriture débit."
            )

        if in_count >= 1:
            print(
                "Écriture crédit vendeur : OK"
            )
        else:
            print(
                "ERREUR écriture crédit."
            )

        # ----------------------------------------------------
        # Rollback volontaire
        # ----------------------------------------------------

        raise RuntimeError(
            "ROLLBACK_STOCK_TEST"
        )

except RuntimeError as exc:

    if str(exc) == "ROLLBACK_STOCK_TEST":
        print("")
        print("=" * 70)
        print("ROLLBACK DU TEST : OK")
        print("=" * 70)

# ------------------------------------------------------------
# Vérification finale après rollback
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
print(" TEST STOCK + PAIEMENT ATOMIQUE : TERMINE")
print("=" * 70)