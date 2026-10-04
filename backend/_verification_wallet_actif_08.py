from pathlib import Path

ROOT = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend")

targets = [
    ROOT / "wenze" / "payment.py",
    ROOT / "wenze" / "views.py",
    ROOT / "finance" / "wallet_service.py",
    ROOT / "wallet" / "models.py",
    ROOT / "wallet" / "services.py",
    ROOT / "wallet" / "views.py",
    ROOT / "wallet" / "views_secure.py",
    ROOT / "wallet" / "signals.py",
    ROOT / "financial_accounts" / "models.py",
]

lines = []

lines.append("=" * 70)
lines.append("NSIKAY - VERIFICATION WALLET ACTIF 08")
lines.append("=" * 70)
lines.append("LECTURE SEULE - AUCUNE MODIFICATION")
lines.append("")

for path in targets:
    lines.append("")
    lines.append("-" * 70)
    lines.append(f"FICHIER : {path}")
    lines.append("-" * 70)

    if not path.exists():
        lines.append("ABSENT")
        continue

    try:
        content = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        for i, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()

            if (
                "from wallet" in stripped
                or "from finance" in stripped
                or "import wallet" in stripped
                or "import finance" in stripped
                or "Wallet.objects" in stripped
                or "WalletBalance" in stripped
                or "WalletCurrencyBalance" in stripped
                or "WalletTransaction" in stripped
                or "credit_wallet" in stripped
                or "debit_wallet" in stripped
                or "transfer_wallet" in stripped
                or "balance" in stripped
                or "GiftFinancialLedger" in stripped
                or "FinancialAccount" in stripped
            ):
                lines.append(f"{i:5} | {line}")

    except Exception as e:
        lines.append(f"ERREUR LECTURE : {e}")

lines.append("")
lines.append("=" * 70)
lines.append("FIN")
lines.append("=" * 70)

Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\reports\gifts\VERIFICATION_WALLET_ACTIF_08.txt").write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print("=" * 70)
print("VERIFICATION WALLET ACTIF 08 TERMINEE")
print("=" * 70)
print("AUCUNE MODIFICATION EFFECTUEE")
print(r"Rapport : C:\Users\DELL Technologies\Desktop\nsikay nante\reports\gifts\VERIFICATION_WALLET_ACTIF_08.txt")