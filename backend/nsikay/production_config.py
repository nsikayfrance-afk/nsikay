import os
from dotenv import load_dotenv

load_dotenv(".env.production")


SECRET_KEY = os.getenv(
    "SECRET_KEY"
)


DEBUG = os.getenv(
    "DEBUG",
    "False"
) == "True"


ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "*"
).split(",")


