import dj_database_url
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== Environment setup =====
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")  # load .env file

DJANGO_ENV = env("DJANGO_ENV", default="development")

# ===== Security =====
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "web"]
)


# ===== Installed apps =====
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_ratelimit",   # rate limiting middleware
    "books",              # your custom app
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

# ===== Database =====
DATABASE_URL = env("DATABASE_URL", default=None)

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env("DB_ENGINE", default="django.db.backends.postgresql"),
            "NAME": env("DB_NAME", default="postgres"),
            "USER": env("DB_USER", default="postgres"),
            "PASSWORD": env("DB_PASSWORD", default=""),
            "HOST": env("DB_HOST", default="localhost"),
            "PORT": env("DB_PORT", default="5432"),
        }
    }

# ===== Redis (Cache & Sessions) =====
if DJANGO_ENV == "production":
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "ssl_cert_reqs": None if env.bool("REDIS_SSL", default=False) else "required",
            },
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/1"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

# ===== Static files =====
STATIC_URL = env("DJANGO_STATIC_URL", default="/static/")

# Match Docker volume mount
STATIC_ROOT = "/app/static"

# Optional: keep extra asset dirs if you have them
STATICFILES_DIRS = [BASE_DIR / "assets"]


# ===== Internationalization =====
LANGUAGE_CODE = env("DJANGO_LANGUAGE_CODE", default="en-us")
TIME_ZONE = env("DJANGO_TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# ===== Default primary key type =====
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===== Auth redirects =====
LOGIN_URL = env("DJANGO_LOGIN_URL", default="login")
LOGIN_REDIRECT_URL = env("DJANGO_LOGIN_REDIRECT_URL", default="books:book_list")
LOGOUT_REDIRECT_URL = env("DJANGO_LOGOUT_REDIRECT_URL", default="login")

# ===== Celery =====
CELERY_BROKER_URL = env("REDIS_URL", default="redis://redis_cache:6379/1")
CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://redis_cache:6379/1")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
