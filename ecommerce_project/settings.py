"""
Django settings for ecommerce_project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: replace this with a real secret before deploying,
# and load it from an environment variable instead of committing it.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-change-me-before-deploying"
)

# SECURITY WARNING: keep DEBUG off in production (set DJANGO_DEBUG=False there).
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*", "127.0.0.1", "localhost"]


INSTALLED_APPS = [
    "django.contrib.staticfiles", 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    "cloudinary_storage", 
    "cloudinary",

    # Project apps
    "accounts",
    "catalog",
    "cart",
    "orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
                "catalog.context_processors.categories",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce_project.wsgi.application"


# Database — PostgreSQL, configured via environment variables so the
# same settings.py works locally and once deployed (e.g. on Render).
# Render provides a single DATABASE_URL; local dev uses the DB_* vars below.
import dj_database_url

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "ecommerce_db"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailAuthBackend",
    "django.contrib.auth.backends.ModelBackend",  # keeps admin login working
]

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "catalog:home"
LOGOUT_REDIRECT_URL = "catalog:home"


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Cairo"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images, fonts from the Electro template)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files: use Cloudinary (free, persistent) when CLOUDINARY_URL is set —
# e.g. once deployed. Locally, with no CLOUDINARY_URL, product images just
# stay on disk under MEDIA_ROOT as before, so nothing changes for local dev.
# if os.environ.get("CLOUDINARY_URL"):
#     DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# STORAGES = {
#     "default": {
#         "BACKEND": (
#             "cloudinary_storage.storage.MediaCloudinaryStorage"
#             if os.environ.get("CLOUDINARY_URL")
#             else "django.core.files.storage.FileSystemStorage"
#         )
#     },
#     "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
# }

# Media files (product images uploaded via the admin)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"