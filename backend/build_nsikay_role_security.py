from pathlib import Path

print("=== SECURISATION DASHBOARDS NSIKAY PAR ROLE ===")


# Création du décorateur sécurité

path = Path("dashboard/security.py")


security_code = """

from functools import wraps

from django.http import JsonResponse

from administration.models import NSIKAYAdminRole



def require_nsikay_role(allowed_roles):


    def decorator(view_func):


        @wraps(view_func)

        def wrapper(request, *args, **kwargs):


            if not request.user.is_authenticated:

                return JsonResponse({

                    "error":
                    "Authentification requise"

                }, status=401)



            try:

                role = NSIKAYAdminRole.objects.get(
                    user=request.user
                )


            except NSIKAYAdminRole.DoesNotExist:


                return JsonResponse({

                    "error":
                    "Aucun rôle NSIKAY associé"

                }, status=403)



            if role.role not in allowed_roles:


                return JsonResponse({

                    "error":
                    "Accès interdit pour ce rôle"

                }, status=403)



            return view_func(
                request,
                *args,
                **kwargs
            )


        return wrapper


    return decorator

"""


path.write_text(
    security_code,
    encoding="utf-8"
)



# Mise à jour views

views = Path("dashboard/views.py")

content = views.read_text(
    encoding="utf-8"
)


if "from .security import require_nsikay_role" not in content:

    content = (
        "from .security import require_nsikay_role\n"
        +
        content
    )



content = content.replace(

"def nsikay_control_center(request):",

"@require_nsikay_role(['SUPER_ADMIN'])\ndef nsikay_control_center(request):"

)



content = content.replace(

"def dashboard_pays(request):",

"@require_nsikay_role(['SUPER_ADMIN','COUNTRY_ADMIN'])\ndef dashboard_pays(request):"

)



content = content.replace(

"def certification_stats(request):",

"@require_nsikay_role(['SUPER_ADMIN','CERTIFICATION_ADMIN'])\ndef certification_stats(request):"

)



content = content.replace(

"def finance_stats(request):",

"@require_nsikay_role(['SUPER_ADMIN','FINANCE_ADMIN'])\ndef finance_stats(request):"

)



content = content.replace(

"def transaction_stats(request):",

"@require_nsikay_role(['SUPER_ADMIN','FINANCE_ADMIN','BANK_ADMIN'])\ndef transaction_stats(request):"

)



views.write_text(
    content,
    encoding="utf-8"
)


print("=== SECURITE ROLE NSIKAY INSTALLEE ===")