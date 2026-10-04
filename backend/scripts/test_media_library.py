from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from media_library.models import (
    MediaAsset,
    MediaDestination,
    MediaDistribution,
)

print()
print("=" * 60)
print("1. VERIFICATION DESTINATIONS")
print("=" * 60)

destinations = list(
    MediaDestination.objects.filter(active=True).order_by("id")
)

print("Destinations actives :", len(destinations))

for d in destinations:
    print(
        f"{d.id:02d} | {d.channel_type:15} | "
        f"{d.name}"
    )

if len(destinations) != 21:
    raise Exception(
        f"21 destinations attendues, {len(destinations)} trouvées."
    )

print()
print("=" * 60)
print("2. PREPARATION UTILISATEUR")
print("=" * 60)

User = get_user_model()

user = (
    User.objects.filter(is_superuser=True)
    .order_by("id")
    .first()
)

if not user:
    user = User.objects.filter(is_staff=True).order_by("id").first()

if not user:
    raise Exception("Aucun utilisateur administrateur disponible.")

print(
    "Utilisateur de test :",
    user.username,
    "| ID =",
    user.id
)

print()
print("=" * 60)
print("3. TEST API UPLOAD")
print("=" * 60)

client = APIClient()
client.force_authenticate(user=user)

test_content = (
    b"NSIKAY MEDIA LIBRARY TEST\n"
    b"Fichier de validation automatique.\n"
)

uploaded = SimpleUploadedFile(
    "nsikay_media_library_test.txt",
    test_content,
    content_type="text/plain",
)

response = client.post(
    "/api/media-library/assets/",
    {
        "title": "NSIKAY TEST - Bibliothèque Média",
        "description": "Test automatique de stockage média NSIKAY.",
        "asset_type": "DOCUMENT",
        "file": uploaded,
    },
    format="multipart",
)

print("HTTP :", response.status_code)

if response.status_code not in [200, 201]:
    print(response.data)
    raise Exception("Création du média échouée.")

asset_id = response.data["id"]

asset = MediaAsset.objects.get(id=asset_id)

print("Asset créé :", asset.id)
print("Titre :", asset.title)
print("Type :", asset.asset_type)
print("Fichier :", asset.file.name)
print("Existe physiquement :", asset.file.storage.exists(asset.file.name))

if not asset.file.storage.exists(asset.file.name):
    raise Exception("Le fichier n'existe pas dans le stockage MEDIA_ROOT.")

print()
print("=" * 60)
print("4. TEST DESTINATIONS MULTIPLES")
print("=" * 60)

wanted_codes = [
    "NSIKAY_TV",
    "SPORT",
    "ENVIRONNEMENT",
    "YOUTUBE",
    "FACEBOOK",
]

selected = list(
    MediaDestination.objects.filter(
        active=True,
        channel_type__in=wanted_codes,
    )
)

print("Destinations sélectionnées :", len(selected))

for d in selected:
    print(
        f"{d.id:02d} | {d.channel_type:15} | {d.name}"
    )

if len(selected) != len(wanted_codes):
    raise Exception(
        "Certaines destinations de test sont introuvables."
    )

response = client.post(
    f"/api/media-library/assets/{asset_id}/set-destinations/",
    {
        "destination_ids": [d.id for d in selected]
    },
    format="json",
)

print()
print("HTTP destinations :", response.status_code)

if response.status_code != 200:
    print(response.data)
    raise Exception("Association des destinations échouée.")

print()
print("=" * 60)
print("5. VERIFICATION DISTRIBUTIONS")
print("=" * 60)

distributions = list(
    MediaDistribution.objects.filter(
        asset_id=asset_id
    ).select_related("destination")
)

print("Distributions créées :", len(distributions))

for dist in distributions:
    print(
        f"{dist.id:02d} | "
        f"{dist.destination.channel_type:15} | "
        f"{dist.destination.name:25} | "
        f"{dist.status}"
    )

if len(distributions) != len(selected):
    raise Exception(
        "Le nombre de distributions ne correspond pas aux destinations."
    )

print()
print("=" * 60)
print("6. TEST RECUPERATION API")
print("=" * 60)

response = client.get(
    f"/api/media-library/assets/{asset_id}/"
)

print("HTTP :", response.status_code)

if response.status_code != 200:
    print(response.data)
    raise Exception("Lecture de l'asset échouée.")

data = response.data

print("Asset API :", data.get("title"))
print("File URL :", data.get("file_url"))
print(
    "Distributions API :",
    len(data.get("distributions", []))
)

if len(data.get("distributions", [])) != len(selected):
    raise Exception(
        "Les distributions ne sont pas correctement retournées par l'API."
    )

print()
print("=" * 60)
print("7. NETTOYAGE DU TEST")
print("=" * 60)

file_name = asset.file.name if asset.file else None

MediaDistribution.objects.filter(asset=asset).delete()

if file_name and asset.file.storage.exists(file_name):
    asset.file.storage.delete(file_name)

asset.delete()

print("Asset de test supprimé.")
print("Distributions de test supprimées.")

print()
print("=" * 60)
print("RESULTAT FINAL")
print("=" * 60)

print("DESTINATIONS      : OK")
print("UPLOAD API        : OK")
print("STOCKAGE FICHIER  : OK")
print("MULTI-DESTINATION : OK")
print("DISTRIBUTIONS     : OK")
print("LECTURE API       : OK")
print("NETTOYAGE         : OK")
print()
print("BIBLIOTHÈQUE MÉDIA : FONCTIONNELLE")
print("=" * 60)
