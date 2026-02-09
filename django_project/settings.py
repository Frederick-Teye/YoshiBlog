import os
import boto3
from decouple import config
import logging.config
from django.utils.log import DEFAULT_LOGGING
from pathlib import Path
import dj_database_url

DJANGO_ENV = os.environ.get("DJANGO_ENV", "local").lower()
IS_LAMBDA = bool(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
IS_PROD = DJANGO_ENV in {"prod", "production", "lambda"} or IS_LAMBDA

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

SECRET_KEY = None

if IS_LAMBDA:
    ssm = boto3.client("ssm", region_name=AWS_REGION)
    try:
        SECRET_KEY = ssm.get_parameter(
            Name="/yoshiblog/secret_key", WithDecryption=True
        )["Parameter"]["Value"]
    except Exception:
        # Fallback for build/test phases if SSM isn't accessible
        SECRET_KEY = os.environ.get("SECRET_KEY") or config("SECRET_KEY")

else:
    SECRET_KEY = os.environ.get("SECRET_KEY") or config(
        "SECRET_KEY", default="django-insecure-key"
    )

DEBUG = not IS_PROD

allowed_hosts_env = os.environ.get("ALLOWED_HOSTS")
if allowed_hosts_env:
    ALLOWED_HOSTS = [
        host.strip() for host in allowed_hosts_env.split(",") if host.strip()
    ]
elif IS_LAMBDA:
    api_gateway_domain = os.environ.get("API_GATEWAY_DOMAIN")
    ALLOWED_HOSTS = [api_gateway_domain] if api_gateway_domain else ["*"]
else:
    ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

csrf_trusted_env = os.environ.get("CSRF_TRUSTED_ORIGINS")
if csrf_trusted_env:
    CSRF_TRUSTED_ORIGINS = [
        origin.strip() for origin in csrf_trusted_env.split(",") if origin.strip()
    ]
elif os.environ.get("API_GATEWAY_DOMAIN"):
    CSRF_TRUSTED_ORIGINS = [f"https://{os.environ.get('API_GATEWAY_DOMAIN')}"]
else:
    CSRF_TRUSTED_ORIGINS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third-party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
    "crispy_forms",
    "crispy_bootstrap5",
    "taggit",
    "storages",
    # Local
    "accounts",
    "pages",
    "blogs.apps.BlogsConfig",
]

if DJANGO_ENV == "local":
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

if DJANGO_ENV == "local":
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Authentication Providers
if IS_LAMBDA:
    ssm = boto3.client("ssm", region_name=AWS_REGION)

    def get_ssm_param(name: str) -> str:
        try:
            return ssm.get_parameter(Name=name, WithDecryption=True)["Parameter"][
                "Value"
            ]
        except Exception:
            return ""

    SOCIALACCOUNT_PROVIDERS = {
        "google": {
            "APP": {
                "client_id": get_ssm_param("/yoshiblog/google_client_id"),
                "secret": get_ssm_param("/yoshiblog/google_secret"),
                "key": "",
            },
            "SCOPE": ["profile", "email"],
            "AUTH_PARAMS": {"access_type": "online"},
        },
        "github": {
            "APP": {
                "client_id": get_ssm_param("/yoshiblog/github_client_id"),
                "secret": get_ssm_param("/yoshiblog/github_secret"),
                "key": "",
            },
            "VERIFIED_EMAIL": True,
        },
    }
else:
    SOCIALACCOUNT_PROVIDERS = {
        "google": {
            "APP": {
                "client_id": config("GOOGLE_CLIENT_ID", default=""),
                "secret": config("GOOGLE_SECRETE", default=""),
                "key": "",
            }
        },
        "github": {
            "APP": {
                "client_id": config("GITHUB_CLIENT_ID", default=""),
                "secret": config("GITHUB_SECRETE", default=""),
                "key": "",
            },
            "VERIFIED_EMAIL": True,
        },
    }

ROOT_URLCONF = "django_project.urls"
WSGI_APPLICATION = "django_project.wsgi.application"

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

# --- DATABASE CONFIGURATION ---
DATABASE_URL = None

if IS_LAMBDA:
    ssm = boto3.client("ssm", region_name=AWS_REGION)
    try:
        # Fetch the SecureString from SSM
        DATABASE_URL = ssm.get_parameter(
            Name="/yoshiblog/database_url", WithDecryption=True
        )["Parameter"]["Value"]
    except Exception as e:
        print(f"Error fetching DATABASE_URL from SSM: {e}")
        DATABASE_URL = None
else:
    # Local development uses .env or environment variable
    DATABASE_URL = os.environ.get("DATABASE_URL") or config(
        "DATABASE_URL", default=None
    )

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL or f"sqlite:///{BASE_DIR}/db.sqlite3",
        conn_max_age=600,
        ssl_require=True if DATABASE_URL and "sqlite" not in DATABASE_URL else False,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (S3)
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME") or config(
    "AWS_STORAGE_BUCKET_NAME", default=None
)
AWS_S3_REGION_NAME = AWS_REGION

if AWS_STORAGE_BUCKET_NAME:
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    }
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }

AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=31536000, immutable"}
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "true").lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL") or config(
    "DEFAULT_FROM_EMAIL", default="root@localhost"
)

if IS_LAMBDA:
    # Attempt to fetch email credentials from SSM if in Lambda
    try:
        EMAIL_HOST = get_ssm_param("/yoshiblog/email_host") or EMAIL_HOST
        EMAIL_HOST_USER = get_ssm_param("/yoshiblog/email_host_user") or EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD = (
            get_ssm_param("/yoshiblog/email_host_password") or EMAIL_HOST_PASSWORD
        )
    except Exception:
        pass

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
    if EMAIL_HOST_USER
    else "django.core.mail.backends.console.EmailBackend"
)

# Django Debug Toolbar
INTERNAL_IPS = ["127.0.0.1", "::1"]
if DJANGO_ENV == "local":
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}

# Auth / AllAuth
AUTH_USER_MODEL = "accounts.CustomUser"
SITE_ID = 1
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

# Logging
LOGGING_CONFIG = None
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO")
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "default"},
        },
        "loggers": {
            "": {"level": "WARNING", "handlers": ["console"]},
            "app": {"level": LOGLEVEL, "handlers": ["console"], "propagate": False},
            "django.server": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }
)

TAGGIT_CASE_INSENSITIVE = True


if IS_LAMBDA:
    # Tell Django it is behind a proxy that handles HTTPS
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
