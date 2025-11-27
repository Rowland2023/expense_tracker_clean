import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_ratelimit',
    "books",  # add the app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_ratelimit.middleware.RateLimitMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "expense_tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # global templates dir (optional)
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
# If DJANGO_ENV=production, use Postgres; else use SQLite
ENV = os.getenv("DJANGO_ENV", "local").lower()

if ENV == "production":
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',  # or the DB name you set during creation
        'USER': 'postgres',
        'PASSWORD': 'God4me2026',
        'HOST': 'database-2.c56oc2ieqd1l.eu-north-1.rds.amazonaws.com',
        'PORT': '5432',
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
STATIC_ROOT = BASE_DIR / "staticfiles"  # for collectstatic in production
STATICFILES_DIRS = [BASE_DIR / "static"]  # optional for local assets


# ===== Cache & sessions (Redis in production) =====

ENV = os.getenv("DJANGO_ENV", "development")

if ENV == "production":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1"),
            "OPTIONS": {
                # If you need SSL, configure properly; here simplified
                "ssl_cert_reqs": None if os.getenv("REDIS_SSL", "false") == "true" else None,
            },
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    # Local dev: simple in-memory cache
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }

# ===== Internationalization (optional) =====
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# ===== Default primary key type =====
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#Configure redirects and messages
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'books:book_list'
LOGOUT_REDIRECT_URL = 'login'
