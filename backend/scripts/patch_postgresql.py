from pathlib import Path

p = Path("nsikay/settings.py")
txt = p.read_text(encoding="utf-8")

old = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

new = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql' if os.environ.get('NSIKAY_ENV') == 'production' else 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DATABASE_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
    }
}"""

if old not in txt:
    raise Exception("ZONE DATABASE INTROUVABLE")

txt = txt.replace(old, new)

p.write_text(txt, encoding="utf-8")

print("DATABASE POSTGRESQL ACTIVE")
