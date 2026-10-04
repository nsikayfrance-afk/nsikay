from pathlib import Path

file = Path("certification/admin.py")

content = file.read_text(encoding="utf-8")


if "NSIKAYCertification" not in content:

    with file.open("a",encoding="utf-8") as f:

        f.write("""

from .models import (
    NSIKAYCertification,
    CertificationHistory
)

admin.site.register(NSIKAYCertification)
admin.site.register(CertificationHistory)

""")


print("=== ADMIN CERTIFICATION AJOUTE ===")