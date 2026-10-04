from django.db import transaction

from .models import FinancialAccount


ACCOUNT_TYPES = [
    ("PRINCIPAL", "Compte principal NSIKAY", "Compte operationnel principal de NSIKAY."),
    ("GIFTS", "Compte cadeaux NSIKAY", "Compte logique de reglement et de tracabilite des cadeaux."),
    ("FEES", "Compte commissions et frais NSIKAY", "Compte logique des revenus et frais effectivement dus a NSIKAY."),
    ("PAYOUT", "Compte retraits NSIKAY", "Compte logique de preparation et de reglement des retraits."),
]

CURRENCIES = ["CDF", "USD", "EUR"]


@transaction.atomic
def seed():

    created = 0
    existing = 0

    for account_type, label, description in ACCOUNT_TYPES:

        for currency in CURRENCIES:

            code = f"NSIKAY-{account_type}-{currency}"

            account, was_created = FinancialAccount.objects.get_or_create(
                code=code,
                defaults={
                    "name": f"{label} - {currency}",
                    "account_type": account_type,
                    "currency": currency,
                    "status": FinancialAccount.AccountStatus.PLANNED,
                    "description": description,
                    "is_internal_ledger": True,
                },
            )

            if was_created:
                created += 1
                print(f"[CREATE] {code}")
            else:
                existing += 1
                print(f"[EXIST]  {code}")

    print("")
    print("==============================================")
    print(" NSIKAY - COMPTES FINANCIERS")
    print("==============================================")
    print(f"Crees     : {created}")
    print(f"Existants : {existing}")
    print("Statut initial : PLANIFIE")
    print("==============================================")


if __name__ == "__main__":
    seed()
