from django.conf import settings
from django.http import FileResponse, Http404


# Build React/Vite embarqué directement dans le backend.
FRONTEND_DIST = settings.BASE_DIR / "frontend_dist"


def frontend_index(request, path=None):
    index_file = FRONTEND_DIST / "index.html"

    if not index_file.exists():
        raise Http404("Frontend NSIKAY non disponible.")

    return FileResponse(
        open(index_file, "rb"),
        content_type="text/html",
    )


def frontend_static(request, path="", folder=""):
    base = FRONTEND_DIST / folder
    file_path = base / path

    try:
        file_path = file_path.resolve()
        base = base.resolve()

        if base != file_path and base not in file_path.parents:
            raise Http404("Fichier frontend invalide.")

    except FileNotFoundError:
        raise Http404("Fichier frontend introuvable.")

    if not file_path.is_file():
        raise Http404("Fichier frontend introuvable.")

    return FileResponse(open(file_path, "rb"))
