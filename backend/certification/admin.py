from django.contrib import admin

# Register your models here.


from .models import (
    NSIKAYCertification,
    CertificationHistory
)

admin.site.register(NSIKAYCertification)
admin.site.register(CertificationHistory)

