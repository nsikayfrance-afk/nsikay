from pathlib import Path

file = Path("nsikay/settings.py")

content = file.read_text(encoding="utf-8")

if "testserver" not in content:

    content = content.replace(
        "ALLOWED_HOSTS = []",
        "ALLOWED_HOSTS = ['localhost','127.0.0.1','testserver']"
    )

file.write_text(content, encoding="utf-8")

print("=== ALLOWED HOSTS CORRIGE ===")


