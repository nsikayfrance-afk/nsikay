from decimal import Decimal
from threading import Barrier, Thread

from django.contrib.auth import get_user_model
from django.db import close_old_connections, connection, transaction

from finance.models import Wallet, WalletTransaction
from wenze.models import WenzeProduct, WenzeOrder
from wenze.payment import pay_wenze_order_with_wallet, WenzePaymentError


User = get_user_model()

print("")
print("=" * 70)
print(" TEST WENZE - PAIEMENT CONCURRENT")
print("=" * 70)

print("")
print("Base de données :", connection.vendor)
print("Moteur :", connection.settings_dict.get("ENGINE"))

if connection.vendor == "sqlite":
    print("")
    print("ATTENTION : SQLite ne permet pas de valider correctement")
    print("le verrouillage concurrent select_for_update().")
    print("Test fonctionnel non exécuté.")
else:

    buyer1 = User.objects.get(
        username="admin_test_nsikay"
    )

    buyer2 = User.objects.get(
        username="banque_test_nsikay"
    )

    seller = User.objects.get(
        username="finance_test_nsikay"
    )

    buyer1_wallet = Wallet.objects.get(
        user=buyer1,
        active=True,
        currency__code="USD",
    )

    buyer2_wallet = Wallet.objects.filter(
        user=buyer2,
        active=True,
    ).first()

    if buyer2_wallet is None:
        raise RuntimeError(
            "Aucun portefeuille actif pour le deuxième acheteur."
        )

    seller_wallet = Wallet.objects.filter(
        user=seller,
        active=True,
    ).first()

    if seller_wallet is None:
        raise RuntimeError(
            "Aucun portefeuille actif vendeur."
        )

    print("")
    print("Acheteur 1 :", buyer1.username)
    print("Wallet 1 :", buyer1_wallet.id, buyer1_wallet.currency.code)

    print("Acheteur 2 :", buyer2.username)
    print("Wallet 2 :", buyer2_wallet.id, buyer2_wallet.currency.code)

    print("Vendeur :", seller.username)
    print("Wallet vendeur :", seller_wallet.id, seller_wallet.currency.code)

    # --------------------------------------------------------
    # Préparation transactionnelle
    # --------------------------------------------------------

    original_buyer1_currency = buyer1_wallet.currency
    original_buyer1_balance = buyer1_wallet.balance

    original_buyer2_currency = buyer2_wallet.currency
    original_buyer2_balance = buyer2_wallet.balance

    original_seller_currency = seller_wallet.currency
    original_seller_balance = seller_wallet.balance

    product = None
    order1 = None
    order2 = None

    try:

        # On prépare les trois wallets dans la même devise.
        buyer2_wallet.currency = buyer1_wallet.currency
        buyer2_wallet.balance = Decimal("1000.00")
        buyer2_wallet.save(
            update_fields=[
                "currency",
                "balance",
            ]
        )

        buyer1_wallet.balance = Decimal("1000.00")
        buyer1_wallet.save(
            update_fields=["balance"]
        )

        seller_wallet.currency = buyer1_wallet.currency
        seller_wallet.balance = Decimal("0.00")
        seller_wallet.save(
            update_fields=[
                "currency",
                "balance",
            ]
        )

        product = WenzeProduct.objects.create(
            seller=seller,
            name="TEST PAIEMENT CONCURRENT",
            description="Produit temporaire - test concurrence",
            price=Decimal("100.00"),
            currency="USD",
            stock=1,
            status="ACTIVE",
        )

        order1 = WenzeOrder.objects.create(
            buyer=buyer1,
            product=product,
            quantity=1,
            unit_price=Decimal("100.00"),
            currency="USD",
            total_amount=Decimal("100.00"),
            reference="TEST-CONCURRENT-001",
        )

        order2 = WenzeOrder.objects.create(
            buyer=buyer2,
            product=product,
            quantity=1,
            unit_price=Decimal("100.00"),
            currency="USD",
            total_amount=Decimal("100.00"),
            reference="TEST-CONCURRENT-002",
        )

        print("")
        print("Stock initial :", product.stock)
        print("Commande 1 :", order1.id, order1.status)
        print("Commande 2 :", order2.id, order2.status)

        # --------------------------------------------------------
        # Lancement simultané
        # --------------------------------------------------------

        barrier = Barrier(2)
        results = {
            "order1": None,
            "order2": None,
        }

        errors = {
            "order1": None,
            "order2": None,
        }

        def pay_order_thread(key, order_id, wallet_id):

            close_old_connections()

            try:

                wallet = Wallet.objects.get(
                    id=wallet_id,
                )

                order = WenzeOrder.objects.get(
                    id=order_id,
                )

                barrier.wait()

                try:

                    result = pay_wenze_order_with_wallet(
                        order=order,
                        buyer_wallet=wallet,
                    )

                    results[key] = {
                        "success": True,
                        "status": result["status"],
                    }

                except WenzePaymentError as exc:

                    results[key] = {
                        "success": False,
                        "error": str(exc),
                    }

                except Exception as exc:

                    errors[key] = (
                        f"{type(exc).__name__}: {exc}"
                    )

            finally:
                close_old_connections()

        thread1 = Thread(
            target=pay_order_thread,
            args=(
                "order1",
                order1.id,
                buyer1_wallet.id,
            ),
        )

        thread2 = Thread(
            target=pay_order_thread,
            args=(
                "order2",
                order2.id,
                buyer2_wallet.id,
            ),
        )

        print("")
        print("Lancement simultané des deux paiements...")

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # --------------------------------------------------------
        # Vérification
        # --------------------------------------------------------

        product.refresh_from_db()
        order1.refresh_from_db()
        order2.refresh_from_db()
        buyer1_wallet.refresh_from_db()
        buyer2_wallet.refresh_from_db()
        seller_wallet.refresh_from_db()

        print("")
        print("=" * 70)
        print(" RESULTATS CONCURRENTS")
        print("=" * 70)

        print("")
        print("Résultat paiement 1 :", results["order1"])
        print("Résultat paiement 2 :", results["order2"])

        if errors["order1"]:
            print(
                "Erreur technique paiement 1 :",
                errors["order1"],
            )

        if errors["order2"]:
            print(
                "Erreur technique paiement 2 :",
                errors["order2"],
            )

        paid_count = WenzeOrder.objects.filter(
            id__in=[order1.id, order2.id],
            status="PAID",
        ).count()

        pending_count = WenzeOrder.objects.filter(
            id__in=[order1.id, order2.id],
            status="PENDING",
        ).count()

        print("")
        print("Commande 1 :", order1.status)
        print("Commande 2 :", order2.status)
        print("Commandes PAID :", paid_count)
        print("Commandes PENDING :", pending_count)
        print("Stock final :", product.stock)

        print("")
        print("Solde acheteur 1 :", buyer1_wallet.balance)
        print("Solde acheteur 2 :", buyer2_wallet.balance)
        print("Solde vendeur :", seller_wallet.balance)

        # --------------------------------------------------------
        # Règles attendues
        # --------------------------------------------------------

        if paid_count == 1:
            print(
                "Une seule commande PAID : OK"
            )
        else:
            print(
                "ERREUR : nombre de commandes PAID =",
                paid_count,
            )

        if pending_count == 1:
            print(
                "Une seule commande reste PENDING : OK"
            )
        else:
            print(
                "ERREUR : nombre de commandes PENDING =",
                pending_count,
            )

        if product.stock == 0:
            print(
                "Stock 1 -> 0 : OK"
            )
        else:
            print(
                "ERREUR stock final :",
                product.stock,
            )

        if product.stock >= 0:
            print(
                "Stock jamais négatif : OK"
            )
        else:
            print(
                "ERREUR : stock négatif."
            )

        if seller_wallet.balance == Decimal("100.00"):
            print(
                "Un seul crédit vendeur de 100 : OK"
            )
        else:
            print(
                "ERREUR crédit vendeur :",
                seller_wallet.balance,
            )

        out_count = WalletTransaction.objects.filter(
            reference__startswith="WENZE-PAY-",
            transaction_type="withdraw",
        ).count()

        in_count = WalletTransaction.objects.filter(
            reference__startswith="WENZE-PAY-",
            transaction_type="deposit",
        ).count()

        print("")
        print("Écritures OUT :", out_count)
        print("Écritures IN :", in_count)

        if out_count == 1:
            print(
                "Un seul débit acheteur : OK"
            )
        else:
            print(
                "ERREUR nombre de débits :",
                out_count,
            )

        if in_count == 1:
            print(
                "Un seul crédit vendeur : OK"
            )
        else:
            print(
                "ERREUR nombre de crédits :",
                in_count,
            )

        # --------------------------------------------------------
        # Rollback complet
        # --------------------------------------------------------

        raise RuntimeError(
            "ROLLBACK_CONCURRENT_TEST"
        )

    except RuntimeError as exc:

        if str(exc) == "ROLLBACK_CONCURRENT_TEST":

            print("")
            print("=" * 70)
            print("ROLLBACK DU TEST CONCURRENT : OK")
            print("=" * 70)

    finally:

        # Si une exception inattendue intervient avant le rollback,
        # les objets temporaires sont supprimés ici.
        if product is not None:

            WenzeOrder.objects.filter(
                id__in=[
                    order1.id if order1 else -1,
                    order2.id if order2 else -1,
                ]
            ).delete()

            WenzeProduct.objects.filter(
                id=product.id
            ).delete()

        # Restauration des wallets.
        buyer1_wallet.currency = original_buyer1_currency
        buyer1_wallet.balance = original_buyer1_balance
        buyer1_wallet.save(
            update_fields=[
                "currency",
                "balance",
            ]
        )

        buyer2_wallet.currency = original_buyer2_currency
        buyer2_wallet.balance = original_buyer2_balance
        buyer2_wallet.save(
            update_fields=[
                "currency",
                "balance",
            ]
        )

        seller_wallet.currency = original_seller_currency
        seller_wallet.balance = original_seller_balance
        seller_wallet.save(
            update_fields=[
                "currency",
                "balance",
            ]
        )

# ------------------------------------------------------------
# Vérification finale
# ------------------------------------------------------------

print("")
print("=" * 70)
print(" VERIFICATION FINALE")
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
print(" TEST PAIEMENT CONCURRENT : TERMINE")
print("=" * 70)