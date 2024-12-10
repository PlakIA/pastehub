import os
from pathlib import Path

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
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static_dev"]

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SHORT_LINK_LENGTH = 8

MAIL = env.str("DJANGO_MAIL", default="default@yandex.ru")

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / "send_mail"
