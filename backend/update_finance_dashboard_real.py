from pathlib import Path

print("=== CONNEXION DASHBOARD FINANCE REEL NSIKAY ===")


path = Path("dashboard/views.py")

content = path.read_text(encoding="utf-8")


start = content.find("def finance_stats")

if start != -1:

    end = content.find("\ndef ", start + 5)

    if end == -1:
        end = len(content)


    old_block = content[start:end]


    new_block = """

def finance_stats(request):

    from finance.models import Currency, ExchangeRate
    from banking.models import Wallet


    devises = []

    for currency in Currency.objects.all():

        devises.append({

            "code":
                getattr(currency, "code", str(currency)),

            "nom":
                str(currency)

        })


    taux = []

    for rate in ExchangeRate.objects.all():

        taux.append({

            "id":
                rate.id,

            "taux":
                getattr(rate, "rate", None),

            "source":
                str(rate)

        })


    wallets = []

    try:

        for wallet in Wallet.objects.all():

            wallets.append({

                "id":
                    wallet.id,

                "proprietaire":
                    str(getattr(wallet, "user", None)),

                "solde":
                    getattr(wallet, "balance", 0),

                "devise":
                    str(getattr(wallet, "currency", ""))

            })

    except Exception:

        wallets = []


    return JsonResponse({

        "module":
            "Finance Réelle NSIKAY",

        "devises":
            len(devises),

        "liste_devises":
            devises,

        "taux_change":
            len(taux),

        "taux":
            taux,

        "portefeuilles":
            len(wallets),

        "wallets":
            wallets,

        "frais_NSIKAY":{

            "transfert":
                "0.25%",

            "retrait":
                "0.50%"

        }

    })

"""


    content = content.replace(old_block,new_block)


else:

    print("fonction finance_stats introuvable")


path.write_text(content, encoding="utf-8")


print("=== DASHBOARD FINANCE REEL CONNECTE ===")