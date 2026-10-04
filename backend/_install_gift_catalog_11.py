import os
from pathlib import Path
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.apps import apps
from django.db import transaction

ROOT = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante")
BACKEND = ROOT / "backend"
MODELS = BACKEND / "api_nsikay" / "models.py"
ADMIN = BACKEND / "api_nsikay" / "admin.py"
SETTINGS = BACKEND / "nsikay" / "settings.py"
URLS = BACKEND / "nsikay" / "urls.py"
SERVICE = BACKEND / "api_nsikay" / "gift_catalog.py"

MEDIA_ROOT = BACKEND / "media"
AVATAR_ROOT = MEDIA_ROOT / "gift_avatars"

REPORT = ROOT / "reports" / "gifts" / "INSTALLATION_CATALOGUE_CADEAUX_11.txt"

lines = []

def log(value=""):
    print(value)
    lines.append(str(value))

def backup(path):
    if path.exists():
        target = path.with_suffix(path.suffix + ".catalogue11.bak")
        target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

# ----------------------------------------------------------------------
# 1. MODELE VIRTUAL GIFT
# ----------------------------------------------------------------------

log("=" * 72)
log("NSIKAY - INSTALLATION CATALOGUE CADEAUX 11")
log("=" * 72)

backup(MODELS)

text = MODELS.read_text(encoding="utf-8")

start = text.find("class VirtualGift(models.Model):")

if start < 0:
    raise RuntimeError("Classe VirtualGift introuvable.")

next_class = text.find("\nclass ", start + 1)

if next_class < 0:
    next_class = len(text)

new_class = '''class VirtualGift(models.Model):
    """
    Catalogue permanent des cadeaux NSIKAY.

    La valeur officielle du catalogue est toujours exprimee en EUR.
    Le champ value/currency est conserve pour compatibilite avec
    l'ancien modele et est synchronise avec value_eur/EUR.
    """

    name = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=180,
        unique=True
    )

    # Compatibilite avec l'ancien systeme.
    value = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=3,
        default="EUR"
    )

    # Nouvelle valeur officielle du catalogue.
    value_eur = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.10")
    )

    currency_reference = models.CharField(
        max_length=3,
        default="EUR"
    )

    avatar = models.FileField(
        upload_to="gift_avatars/",
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=80,
        default="MINERAL"
    )

    active = models.BooleanField(
        default=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    metadata = models.JSONField(
        default=dict,
        blank=True
    )

    class Meta:
        ordering = ["display_order", "value_eur", "id"]
        indexes = [
            models.Index(fields=["active", "display_order"]),
            models.Index(fields=["currency_reference", "value_eur"]),
            models.Index(fields=["category", "active"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.value_eur} EUR"

    @property
    def reference_value_eur(self):
        return self.value_eur
'''

text = text[:start] + new_class + text[next_class:]

MODELS.write_text(text, encoding="utf-8")

log("MODELE VirtualGift enrichi.")

# ----------------------------------------------------------------------
# 2. SETTINGS MEDIA
# ----------------------------------------------------------------------

backup(SETTINGS)

settings_text = SETTINGS.read_text(encoding="utf-8")

if "MEDIA_ROOT" not in settings_text:
    settings_text += """

# ============================================================
# NSIKAY - MEDIA CADEAUX
# ============================================================
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
"""

else:
    if "MEDIA_URL" not in settings_text:
        settings_text += '\nMEDIA_URL = "/media/"\n'
    if "MEDIA_ROOT" not in settings_text:
        settings_text += '\nMEDIA_ROOT = BASE_DIR / "media"\n'

SETTINGS.write_text(settings_text, encoding="utf-8")

log("MEDIA_ROOT / MEDIA_URL prepares.")

# ----------------------------------------------------------------------
# 3. URLS MEDIA EN DEVELOPPEMENT
# ----------------------------------------------------------------------

backup(URLS)

urls_text = URLS.read_text(encoding="utf-8")

if "from django.conf import settings" not in urls_text:
    urls_text = "from django.conf import settings\n" + urls_text

if "from django.conf.urls.static import static" not in urls_text:
    urls_text = "from django.conf.urls.static import static\n" + urls_text

if "static(settings.MEDIA_URL" not in urls_text:
    urls_text += """

# NSIKAY - fichiers media en environnement de developpement
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
"""

URLS.write_text(urls_text, encoding="utf-8")

log("Routes MEDIA preparees.")

# ----------------------------------------------------------------------
# 4. SERVICE DE CONVERSION EUR -> DEVISE PRINCIPALE
# ----------------------------------------------------------------------

SERVICE.write_text(r'''from decimal import Decimal
from django.apps import apps


REFERENCE_CURRENCY = "EUR"
SUPPORTED_DISPLAY_CURRENCIES = ("EUR", "USD", "CDF")


def _field_names(model):
    return {field.name for field in model._meta.fields}


def get_exchange_rate(target_currency):
    """
    Retourne le taux EUR -> devise cible depuis finance.ExchangeRate.

    La structure existante du modele ExchangeRate pouvant evoluer,
    le service detecte les noms de champs usuels au lieu de figer
    une structure non verifiee.
    """

    target_currency = str(target_currency).upper()

    if target_currency == REFERENCE_CURRENCY:
        return Decimal("1")

    ExchangeRate = apps.get_model("finance", "ExchangeRate")
    fields = _field_names(ExchangeRate)

    source_names = [
        "base_currency",
        "from_currency",
        "source_currency",
        "currency_from",
    ]

    target_names = [
        "target_currency",
        "to_currency",
        "destination_currency",
        "currency_to",
    ]

    rate_names = [
        "rate",
        "exchange_rate",
        "value",
        "rate_value",
    ]

    source_field = next(
        (name for name in source_names if name in fields),
        None
    )

    target_field = next(
        (name for name in target_names if name in fields),
        None
    )

    rate_field = next(
        (name for name in rate_names if name in fields),
        None
    )

    if not source_field or not target_field or not rate_field:
        raise LookupError(
            "Structure ExchangeRate incompatible avec le service "
            "de conversion EUR -> devise principale."
        )

    queryset = ExchangeRate.objects.all()

    source_value = "EUR"
    target_value = target_currency

    queryset = queryset.filter(
        **{
            source_field: source_value,
            target_field: target_value,
        }
    )

    row = queryset.order_by("-id").first()

    if row is None:
        raise LookupError(
            f"Taux EUR -> {target_currency} introuvable."
        )

    rate = Decimal(str(getattr(row, rate_field)))

    if rate <= 0:
        raise ValueError(
            f"Taux EUR -> {target_currency} invalide."
        )

    return rate


def convert_gift_value(value_eur, target_currency):
    """
    Convertit une valeur catalogue EUR vers la devise principale
    de l'utilisateur.
    """

    value_eur = Decimal(str(value_eur))
    target_currency = str(target_currency).upper()

    if target_currency not in SUPPORTED_DISPLAY_CURRENCIES:
        raise ValueError(
            f"Devise d'affichage non prise en charge : {target_currency}"
        )

    rate = get_exchange_rate(target_currency)

    return {
        "currency": target_currency,
        "value": (value_eur * rate).quantize(Decimal("0.01")),
        "reference_currency": "EUR",
        "reference_value": value_eur,
        "rate": rate,
    }
''', encoding="utf-8")

log("Service de conversion cree.")

# ----------------------------------------------------------------------
# 5. ADMINISTRATION
# ----------------------------------------------------------------------

backup(ADMIN)

admin_text = ADMIN.read_text(encoding="utf-8")

if "VirtualGift" not in admin_text:
    admin_text += '''

from django.contrib import admin
from .models import VirtualGift

@admin.register(VirtualGift)
class VirtualGiftAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "value_eur",
        "currency_reference",
        "category",
        "active",
        "display_order",
    )
    list_filter = (
        "active",
        "category",
        "currency_reference",
    )
    search_fields = (
        "name",
        "slug",
    )
    ordering = (
        "display_order",
        "value_eur",
    )
    readonly_fields = ()
'''

ADMIN.write_text(admin_text, encoding="utf-8")

log("Administration VirtualGift preparee.")

# ----------------------------------------------------------------------
# 6. DOSSIERS
# ----------------------------------------------------------------------

AVATAR_ROOT.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# 7. DONNEES CATALOGUE
# ----------------------------------------------------------------------

VirtualGift = apps.get_model("api_nsikay", "VirtualGift")

catalogue = [
    ("Quartz", "quartz", "0.10", "CRISTAL"),
    ("Calcite", "calcite", "0.20", "MINERAL"),
    ("Fluorite", "fluorite", "0.50", "MINERAL"),
    ("Obsidienne", "obsidienne", "1.00", "ROCHE"),
    ("Améthyste", "amethyste", "2.00", "GEMME"),
    ("Grenat", "grenat", "5.00", "GEMME"),
    ("Topaze", "topaze", "10.00", "GEMME"),
    ("Aigue-marine", "aigue_marine", "20.00", "GEMME"),
    ("Émeraude", "emeraude", "50.00", "GEMME"),
    ("Saphir", "saphir", "100.00", "GEMME"),
    ("Rubis", "rubis", "200.00", "GEMME"),
    ("Or", "or", "500.00", "METAL"),
    ("Platine", "platine", "1000.00", "METAL"),
    ("Palladium", "palladium", "2500.00", "METAL"),
    ("Diamant", "diamant", "5000.00", "GEMME"),
    ("Diamant Noir", "diamant_noir", "10000.00", "GEMME"),
    ("Diamant Bleu", "diamant_bleu", "25000.00", "GEMME"),
    ("Diamant Royal", "diamant_royal", "50000.00", "GEMME"),
    ("Diamant Impérial", "diamant_imperial", "100000.00", "GEMME"),
]

created = 0
updated = 0

with transaction.atomic():
    for order, (name, slug, value, category) in enumerate(
        catalogue,
        start=1
    ):
        value_decimal = Decimal(value)

        obj, was_created = VirtualGift.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name,
                "value": value_decimal,
                "currency": "EUR",
                "value_eur": value_decimal,
                "currency_reference": "EUR",
                "category": category,
                "active": True,
                "display_order": order,
                "metadata": {
                    "catalogue": "NSIKAY",
                    "reference_currency": "EUR",
                    "avatar_key": slug,
                    "permanent_catalogue": True,
                    "stock": False,
                },
            }
        )

        if was_created:
            created += 1
        else:
            updated += 1

        avatar_path = AVATAR_ROOT / f"{slug}.svg"

        # Avatar SVG provisoire original.
        # Il sera remplace par l'illustration graphique finale
        # sans modifier le cadeau ni sa valeur.
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
 width="512" height="512" viewBox="0 0 512 512">
 <defs>
   <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
     <stop offset="0%" stop-color="#ffffff"/>
     <stop offset="45%" stop-color="#d9e2ec"/>
     <stop offset="100%" stop-color="#7b8794"/>
   </linearGradient>
   <filter id="s">
     <feDropShadow dx="0" dy="12" stdDeviation="12"
       flood-opacity=".28"/>
   </filter>
 </defs>
 <circle cx="256" cy="256" r="218"
   fill="#f4f6f8"/>
 <path d="M256 72
          L392 180
          L348 378
          L256 438
          L164 378
          L120 180 Z"
   fill="url(#g)"
   stroke="#20252b"
   stroke-width="10"
   filter="url(#s)"/>
 <path d="M256 72 L256 438
          M120 180 L392 180
          M164 378 L348 378"
   stroke="#ffffff"
   stroke-opacity=".65"
   stroke-width="8"
   fill="none"/>
</svg>'''

        avatar_path.write_text(
            svg,
            encoding="utf-8"
        )

        relative_avatar = f"gift_avatars/{slug}.svg"

        if not obj.avatar:
            obj.avatar.name = relative_avatar
            obj.save(update_fields=["avatar"])

log(f"CADEAUX CREES : {created}")
log(f"CADEAUX MIS A JOUR : {updated}")
log(f"TOTAL CATALOGUE : {VirtualGift.objects.count()}")
log(f"AVATARS : {len(catalogue)}")

# ----------------------------------------------------------------------
# 8. VALIDATION
# ----------------------------------------------------------------------

invalid = VirtualGift.objects.filter(
    value_eur__lt=Decimal("0.10")
).count()

too_high = VirtualGift.objects.filter(
    value_eur__gt=Decimal("100000.00")
).count()

non_eur = VirtualGift.objects.exclude(
    currency_reference="EUR"
).count()

missing_avatar = VirtualGift.objects.filter(
    avatar=""
).count()

log("")
log("=" * 72)
log("VALIDATION CATALOGUE")
log("=" * 72)
log(f"VALEURS < 0,10 EUR : {invalid}")
log(f"VALEURS > 100000 EUR : {too_high}")
log(f"REFERENCE NON EUR : {non_eur}")
log(f"AVATARS MANQUANTS : {missing_avatar}")

if invalid or too_high or non_eur or missing_avatar:
    raise RuntimeError(
        "Validation catalogue echouee."
    )

for gift in VirtualGift.objects.order_by("display_order"):
    log(
        f"{gift.display_order:02d} | "
        f"{gift.name} | "
        f"{gift.value_eur} EUR | "
        f"{gift.avatar.name}"
    )

REPORT.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print("")
print("=" * 72)
print("INSTALLATION CATALOGUE CADEAUX 11 TERMINEE")
print("=" * 72)
print(f"Rapport : {REPORT}")