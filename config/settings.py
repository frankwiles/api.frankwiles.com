import environs
import logging
import structlog
import sys

from django.core.exceptions import ImproperlyConfigured
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent
APPS_DIR = BASE_DIR.joinpath("config")

#############################################################################
# Environment
#############################################################################
env = environs.Env()

# We shouldn't load a .env file in any deployed context and rely on the
# container orchestration to inject values into the running environment
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    env.read_env()
    print("The .env file has been loaded. See config/settings.py for more information")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)

LOG_LEVEL = env.log_level("LOG_LEVEL", default="INFO")

# Wether or not we're running in a local development environment or not
LOCAL_DEVELOPMENT = env.bool("LOCAL_DEVELOPMENT", False)

# Wether or not to use whitenoise
USE_WHITENOISE = env.bool("USE_WHITENOISE", default=DEBUG)

# Whether celery is eager or not
CELERY_ALWAYS_EAGER = env.bool("CELERY_ALWAYS_EAGER", default=False)

#############################################################################
# Main Settings
#############################################################################
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

#############################################################################
# Security Settings
#############################################################################
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

host_list = env.list("ALLOWED_HOSTS", default="localhost")
ALLOWED_HOSTS = [el.strip() for el in host_list]

#############################################################################
# Installed Apps
#############################################################################
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Third-party apps
INSTALLED_APPS += [
    "django_extensions",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.celery",
]

# Our Apps
INSTALLED_APPS += ["ak", "users", "counters", "core"]


#############################################################################
# Middleware
#############################################################################
MIDDLEWARE = [
    "tracer.middleware.RequestID",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    "django_structlog.middlewares.CeleryMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.joinpath("templates").as_posix()],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


#############################################################################
# Authentication
#############################################################################
AUTH_USER_MODEL = "users.User"

# Password validation
# Only used in production
AUTH_PASSWORD_VALIDATORS = []

#############################################################################
# Database
#############################################################################
try:
    DATABASES = {"default": env.dj_db_url("DATABASE_URL")}
except (ImproperlyConfigured, environs.EnvError):
    DATABASES = {
        "default": {
            "ENGINE": "django_db_geventpool.backends.postgresql_psycopg2",
            "HOST": env("PGHOST"),
            "NAME": env("PGDATABASE"),
            "PASSWORD": env("PGPASSWORD"),
            "PORT": env.int("PGPORT", default=5432),
            "USER": env("PGUSER"),
            "CONN_MAX_AGE": 0,
            "OPTIONS": {"MAX_CONNS": 100},
        }
    }

# Default auto keys
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

#############################################################################
# Sessions
#############################################################################

# Use cached sessions by default
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_COOKIE_NAME = "config-sessionid"

# Increase default cookie age from 2 to 12 weeks
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 12

#############################################################################
# Internationalization
#############################################################################
LANGUAGE_CODE = "en-us"
USE_I18N = True
TIME_ZONE = "UTC"
USE_TZ = True


#############################################################################
# Static files (CSS, JavaScript, Images)
#############################################################################
# The relative URL of where we serve our static files from
STATIC_URL = "/static/"

# Additional directories from where we should collect static files from
STATICFILES_DIRS = [BASE_DIR.joinpath("static").as_posix()]

# This is the directory where all of the collected static files are put
# after running collectstatic
STATIC_ROOT = BASE_DIR.joinpath("deployed_static").as_posix()

# Use Whitenoise if debug is on
if USE_WHITENOISE:
    # These are necessary to turn on Whitenoise which will serve our static
    # files while doing local development
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True


#############################################################################
# Logging setup
#############################################################################
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)
root.addHandler(handler)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["event", "logger"]
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
        "kv": {
            "class": "logging.StreamHandler",
            "formatter": "key_value",
        },
    },
    "loggers": {
        "": {
            "handlers": ["json"],
            "level": LOG_LEVEL,  # defaults to INFO
        },
    },
}

# Configure struct log
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

#############################################################################
# Configure Redis
#############################################################################
REDIS_HOST = env.str("REDIS_HOST", default="redis")
REDIS_PORT = env.int("REDIS_PORT", default=6379)

#############################################################################
# Cache Setup
#############################################################################
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
    }
}

#############################################################################
# Configure Celery
#############################################################################
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_ALWAYS_EAGER = CELERY_ALWAYS_EAGER  # from the env, defaults to False

#############################################################################
# Configure Email (defaults to local maildev service)
#############################################################################
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL", default="testing@localhost")
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = env("DJANGO_EMAIL_HOST", default="maildev")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER", default="")
EMAIL_PORT = env.int("DJANGO_EMAIL_PORT", default=25)
EMAIL_USE_TLS = env.bool("DJANGO_EMAIL_USE_TLS", default=False)
