from django.urls import resolve, reverse, NoReverseMatch
from django.conf import settings
from django.urls.resolvers import URLPattern, URLResolver

print("")
print("=" * 60)
print(" NSIKAY - DIAGNOSTIC REEL DES ROUTES ACTIVITES")
print("=" * 60)

print("")
print("[1] URLCONF PRINCIPAL")
print("ROOT_URLCONF =", settings.ROOT_URLCONF)

print("")
print("[2] ROUTES DETECTEES")

def inspect_patterns(patterns, prefix=""):
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            current = prefix + str(pattern.pattern)
            print("[GROUP]", current)
            inspect_patterns(pattern.url_patterns, current)

        elif isinstance(pattern, URLPattern):
            route = prefix + str(pattern.pattern)
            name = pattern.name or "(sans nom)"

            print("[ROUTE]")
            print("  path =", route)
            print("  name =", name)

            if "activ" in route.lower() or "activ" in name.lower():
                print("  >>> ACTIVITES <<<")

try:
    from django.urls import get_resolver

    resolver = get_resolver()
    inspect_patterns(resolver.url_patterns)

except Exception as e:
    print("[ERREUR INSPECTION ROUTES]")
    print(type(e).__name__, str(e))

print("")
print("[3] TEST REVERSE")

names_to_test = [
    "activites",
    "activite",
    "activities",
    "activity",
    "api:activites",
    "api:activite",
    "api:activities",
    "api:activity",
]

for name in names_to_test:
    try:
        result = reverse(name)
        print("[OK]", name, "=>", result)
    except NoReverseMatch:
        print("[--]", name, "=> aucune route")
    except Exception as e:
        print("[ERR]", name, "=>", type(e).__name__, str(e))

print("")
print("=" * 60)
print(" FIN DIAGNOSTIC ")
print("=" * 60)