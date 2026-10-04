from django.contrib import admin
from .models import (
    BankCertification,
    CurrencyApproval,
    ValidationRequest,
    CountrySupervision
)

admin.site.register(BankCertification)
admin.site.register(CurrencyApproval)
admin.site.register(ValidationRequest)
admin.site.register(CountrySupervision)


from .models import (
    BankPartner,
    BankPartnerCurrency,
    BankPartnerService
)

admin.site.register(BankPartner)
admin.site.register(BankPartnerCurrency)
admin.site.register(BankPartnerService)



from .models import (
    CountryCurrencyAccess,
    CountryRegulation,
    CountryBankAccess
)

admin.site.register(CountryCurrencyAccess)
admin.site.register(CountryRegulation)
admin.site.register(CountryBankAccess)


