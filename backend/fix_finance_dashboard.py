from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

content = content.replace(
"""
        from finance.models import *


        return JsonResponse({

            "module": "Statistiques Financières NSIKAY",

            "status": "connecte"

        })
""",
"""
        from finance import models as finance_models


        return JsonResponse({

            "module": "Statistiques Financières NSIKAY",

            "status": "connecte",

            "models": [
                name for name in dir(finance_models)
                if not name.startswith("_")
            ]

        })
"""
)

file.write_text(content, encoding="utf-8")

print("=== CORRECTION FINANCE DASHBOARD TERMINEE ===")


