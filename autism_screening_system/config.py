import os
from dotenv import load_dotenv


# Always load .env from the same folder as this config.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)


def env_bool(name, default=False):
    return os.getenv(
        name,
        str(default)
    ).strip().lower() in {"1", "true", "yes", "on"}


# Flask
FLASK_SECRET_KEY = os.getenv(
    "FLASK_SECRET_KEY"
) or "development-only-change-me"


# Email
EMAIL_ENABLED = env_bool("EMAIL_ENABLED")

EMAIL_PROVIDER = os.getenv(
    "EMAIL_PROVIDER",
    "gmail"
)

GMAIL_EMAIL = os.getenv(
    "GMAIL_EMAIL",
    ""
)

GMAIL_APP_PASSWORD = os.getenv(
    "GMAIL_APP_PASSWORD",
    ""
)

DOCTOR_EMAIL = os.getenv(
    "DOCTOR_EMAIL",
    ""
)

REPORT_RECIPIENT_EMAIL = os.getenv(
    "REPORT_RECIPIENT_EMAIL",
    DOCTOR_EMAIL
)



