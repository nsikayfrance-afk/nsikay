from pathlib import Path

file = Path("service_dashboard/dashboard_views.py")
text = file.read_text(encoding="utf-8")

patch = Path("service_dashboard/activation_patch.py").read_text(
    encoding="utf-8"
)

start = patch.find("@user_passes_test(is_nsikay_admin)\ndef activate_service")
end = patch.find("\n\npython manage.py check")

if start == -1:
    raise SystemExit("Fonctions d'activation introuvables dans le patch.")

activation_code = patch[start:end].strip()

names = [
    "def activate_service(",
    "def deactivate_service(",
]

for name in names:
    if name in text:
        raise SystemExit(
            f"{name} existe deja dans dashboard_views.py. "
            "Integration automatique interrompue pour eviter un doublon."
        )

text = text.rstrip() + "\n\n\n" + activation_code + "\n"

file.write_text(text, encoding="utf-8")

print("=== ACTIVATION ADMIN NSIKAY INTEGREE ===")

