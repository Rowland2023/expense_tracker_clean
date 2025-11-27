import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== Environment setup =====
env = environ.Env()
environ.Env.read_env()  # reads .env file

# ===== Security =====
SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-secret-key")
DEBUG = env.bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# ===== Installed apps =====
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_ratelimit",
    "books",  # your custom app
]

# ===== Middleware =====
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "expense_tracker.urls"

# ===== Templates =====
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

WSGI_APPLICATION = "expense_tracker.wsgi.application"

# ===== Databases =====
DJANGO_ENV = env("DJANGO_ENV", default="local").lower()

if DJANGO_ENV == "production":
    DATABASES = {
        "default": {
            "ENGINE": env("DB_ENGINE"),
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ===== Static files =====
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ===== Cache & sessions =====
# settings.py

# This package must be installed: pip install django-redis

if DJANGO_ENV == "production":
    CACHES = {
        "default": {
            # Production uses django_redis.cache.RedisCache (or similar path depending on your Redis library)
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/1"),
            "OPTIONS": {
                "ssl_cert_reqs": None if env.bool("REDIS_SSL", default=False) else None,
                "CLIENT_CLASS": "django_redis.client.DefaultClient", # Ensure client class is specified for consistency
            },
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    # --- CHANGE IS HERE ---
    # Use Redis for development/testing to support django-ratelimit's atomic operations.
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            # This default URL should point to a Redis instance running locally (like via Docker or a local installation).
            "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/1"), 
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

# Ensure django_ratelimit is in INSTALLED_APPS and middleware is set up!
# ===== Internationalization =====
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# ===== Default primary key type =====
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===== Auth redirects =====
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "books:book_list"
LOGOUT_REDIRECT_URL = "login"


