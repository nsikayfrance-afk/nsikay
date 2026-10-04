import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

django.setup()


from administration.models import (
    BankPartner,
    BankPartnerCurrency,
    BankPartnerService
)


banks = [

    {
        "name":"NSIKAY Bank RDC",
        "country":"RDC",
        "code":"NSK-RDC",
        "certified":True,
        "currencies":["CDF","USD"],
        "services":[
            "deposit",
            "withdraw",
            "transfer",
            "wallet"
        ]
    },

    {
        "name":"NSIKAY Bank International",
        "country":"International",
        "code":"NSK-INT",
        "certified":True,
        "currencies":["EUR","USD"],
        "services":[
            "transfer",
            "exchange",
            "wallet"
        ]
    }

]


for item in banks:

    bank, created = BankPartner.objects.get_or_create(

        code=item["code"],

        defaults={
            "name":item["name"],
            "country":item["country"],
            "certified":item["certified"]
        }

    )


    for currency in item["currencies"]:

        BankPartnerCurrency.objects.get_or_create(

            bank=bank,
            currency=currency

        )


    for service in item["services"]:

        BankPartnerService.objects.get_or_create(

            bank=bank,
            service=service

        )


print("=== BANQUES PARTENAIRES NSIKAY CREEES ===")