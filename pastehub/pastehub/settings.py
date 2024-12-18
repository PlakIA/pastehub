import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
import environ

env = environ.Env()
environ.Env.read_env(
    os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("DJANGO_SECRET_KEY", default="SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])

INTERNAL_IPS = env.list("DJANGO_INTERNAL_IPS", default=["127.0.0.1"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "core.apps.CoreConfig",
    "paste.apps.PasteConfig",
    "users.apps.UsersConfig",
    "report.apps.ReportConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

ROOT_URLCONF = "pastehub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pastehub.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
        ),
    },
]

AUTH_USER_MODEL = "users.CustomUser"

DEFAULT_USER_IS_ACTIVE = env.bool(
    "DJANGO_DEFAULT_USER_IS_ACTIVE",
    default=False,
)

LANGUAGE_CODE = "ru-ru"

LANGUAGES = [
    ("en", _("Английский")),
    ("ru", _("Русский")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

TIME_ZONE = env("DJANGO_TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True

DATA_UPLOAD_MAX_MEMORY_SIZE = env.int(
    "DJANGO_MAX_UPLOAD",
    default=20 * 1024 * 1024,
)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static_dev"]

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SHORT_LINK_LENGTH = env.int("DJANGO_SHORT_LINK_LENGTH", default=8)

DEFAULT_FROM_EMAIL = env.str(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="default@test.py",
)

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / "send_mail"

if not DEBUG:
    INSTALLED_APPS += ["storages"]

    AWS_ACCESS_KEY_ID = env("S3_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("S3_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = env("S3_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("S3_REGION", default="ru-central1")
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_ENDPOINT_URL = env(
        "S3_ENDPOINT_URL",
        default="https://storage.yandexcloud.net",
    )

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "location": "media",
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "location": "static",
            },
        },
    }

    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/"
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/static/"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
            "OPTIONS": {
                "sslmode": "verify-full",
                "sslrootcert": env(
                    "DB_CERT_PATH",
                    default=BASE_DIR / "db_root.crt",
                ),
            },
        },
    }

    CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST", default="postbox.cloud.yandex.net")
    EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
    EMAIL_HOST_USER = env("EMAIL_USER", default="API_KEY")
    EMAIL_PORT = 587
    DEFAULT_FROM_EMAIL = env.str(
        "DJANGO_DEFAULT_FROM_EMAIL",
        default="no-reply@paste-hub.ru",
    )
    EMAIL_USE_TLS = True
