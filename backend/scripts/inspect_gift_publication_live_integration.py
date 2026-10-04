import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.apps import apps


print("")
print("=" * 80)
print(" NSIKAY - INSPECTION PUBLICATIONS / LIVES / CADEAUX")
print("=" * 80)

# ----------------------------------------------------------------------
# MODELES CANDIDATS
# ----------------------------------------------------------------------

keywords = [
    "post",
    "publication",
    "live",
    "stream",
    "gift",
    "gifttransaction",
    "financial",
    "ledger",
    "creator",
]

print("")
print("===== MODELES DJANGO PERTINENTS =====")

for model in sorted(apps.get_models(), key=lambda m: f"{m._meta.app_label}.{m.__name__}"):

    label = f"{model._meta.app_label}.{model.__name__}"

    if any(k in label.lower() for k in keywords):

        print("")
        print(f"[{label}]")
        print(f"table = {model._meta.db_table}")

        for field in model._meta.fields:

            relation = ""

            if field.is_relation:
                relation = (
                    f" -> {field.remote_field.model._meta.label}"
                )

            print(
                f"  - {field.name:30s} "
                f"{field.__class__.__name__:25s}"
                f"{relation}"
            )

# ----------------------------------------------------------------------
# TABLES REELLES
# ----------------------------------------------------------------------

print("")
print("===== COMPTAGES =====")

targets = []

for model in apps.get_models():

    label = f"{model._meta.app_label}.{model.__name__}"

    if any(k in label.lower() for k in keywords):
        targets.append(model)

for model in sorted(
    targets,
    key=lambda m: f"{m._meta.app_label}.{m.__name__}"
):

    try:
        count = model.objects.count()
    except Exception as exc:
        count = f"ERREUR: {exc}"

    print(
        f"{model._meta.label:45s} "
        f"count={count}"
    )

# ----------------------------------------------------------------------
# GiftTransaction
# ----------------------------------------------------------------------

print("")
print("===== GIFTTRANSACTION =====")

try:

    GiftTransaction = apps.get_model(
        "api_nsikay",
        "GiftTransaction"
    )

    print("Table :", GiftTransaction._meta.db_table)
    print("Nombre :", GiftTransaction.objects.count())

    for field in GiftTransaction._meta.fields:

        relation = ""

        if field.is_relation:
            relation = (
                f" -> {field.remote_field.model._meta.label}"
            )

        print(
            f"{field.name:30s} "
            f"{field.__class__.__name__:25s}"
            f"{relation}"
        )

except Exception as exc:

    print("GiftTransaction indisponible :", exc)

# ----------------------------------------------------------------------
# SocialPost
# ----------------------------------------------------------------------

print("")
print("===== SOCIALPOST =====")

try:

    SocialPost = apps.get_model(
        "api_nsikay",
        "SocialPost"
    )

    print("Table :", SocialPost._meta.db_table)
    print("Nombre :", SocialPost.objects.count())

    for field in SocialPost._meta.fields:

        relation = ""

        if field.is_relation:
            relation = (
                f" -> {field.remote_field.model._meta.label}"
            )

        print(
            f"{field.name:30s} "
            f"{field.__class__.__name__:25s}"
            f"{relation}"
        )

except Exception as exc:

    print("SocialPost indisponible :", exc)

# ----------------------------------------------------------------------
# TV / LIVE
# ----------------------------------------------------------------------

print("")
print("===== MODELES TV / LIVE =====")

for model in sorted(apps.get_models(), key=lambda m: m.__name__):

    name = model.__name__.lower()
    label = f"{model._meta.app_label}.{model.__name__}".lower()

    if (
        "live" in name
        or "stream" in name
        or "live" in label
        or "stream" in label
    ):

        print("")
        print(
            f"[{model._meta.label}] "
            f"table={model._meta.db_table}"
        )

        for field in model._meta.fields:

            relation = ""

            if field.is_relation:
                relation = (
                    f" -> {field.remote_field.model._meta.label}"
                )

            print(
                f"  - {field.name:30s} "
                f"{field.__class__.__name__:25s}"
                f"{relation}"
            )

# ----------------------------------------------------------------------
# FINANCE / GIFT LEDGER
# ----------------------------------------------------------------------

print("")
print("===== FINANCIAL GIFT LEDGER =====")

try:

    GiftFinancialLedger = apps.get_model(
        "financial_accounts",
        "GiftFinancialLedger"
    )

    print(
        "Table :",
        GiftFinancialLedger._meta.db_table
    )

    print(
        "Nombre :",
        GiftFinancialLedger.objects.count()
    )

    for field in GiftFinancialLedger._meta.fields:

        relation = ""

        if field.is_relation:
            relation = (
                f" -> {field.remote_field.model._meta.label}"
            )

        print(
            f"  - {field.name:30s} "
            f"{field.__class__.__name__:25s}"
            f"{relation}"
        )

except Exception as exc:

    print("GiftFinancialLedger indisponible :", exc)

print("")
print("=" * 80)
print(" FIN INSPECTION")
print("=" * 80)