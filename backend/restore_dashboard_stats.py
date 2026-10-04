from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

add = """

@login_required
def dashboard_stats(request):

    from django.contrib.auth import get_user_model

    User = get_user_model()

    return JsonResponse({

        "module": "NSIKAY Dashboard Statistics",

        "utilisateurs": User.objects.count(),

        "statut": "connecte"

    })

"""

if "def dashboard_stats" not in content:

    content += add

    file.write_text(content, encoding="utf-8")


print("=== DASHBOARD STATS RESTAURE ===")


