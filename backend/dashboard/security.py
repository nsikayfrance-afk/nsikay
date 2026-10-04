

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

