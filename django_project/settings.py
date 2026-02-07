import os
import boto3
from decouple import config
import logging.config
from django.utils.log import DEFAULT_LOGGING
from pathlib import Path

DJANGO_ENV = os.environ.get("DJANGO_ENV", "local").lower()
IS_LAMBDA = bool(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
IS_PROD = DJANGO_ENV in {"prod", "production", "lambda"} or IS_LAMBDA


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

if IS_LAMBDA:  # In Lambda
    ssm = boto3.client("ssm", region_name=AWS_REGION)
    SECRET_KEY = ssm.get_parameter(Name="/yoshiblog/secret_key", WithDecryption=True)[
        "Parameter"
    ]["Value"]
else:
    SECRET_KEY = os.environ.get("SECRET_KEY") or config("SECRET_KEY")


# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PROD


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
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
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
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

# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # django-allauth
]

if DJANGO_ENV == "local":
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")


# Provider specific settings
if IS_LAMBDA:  # In Lambda
    ssm = boto3.client("ssm", region_name=AWS_REGION)

    def get_ssm_param(name: str) -> str:
        return ssm.get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]

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
            # For each OAuth based provider, either add a ``SocialApp``
            # (``socialaccount`` app) containing the required client
            # credentials, or list them here:
            "APP": {
                "client_id": os.environ.get("GOOGLE_CLIENT_ID")
                or config("GOOGLE_CLIENT_ID"),
                "secret": os.environ.get("GOOGLE_SECRETE") or config("GOOGLE_SECRETE"),
                "key": "",
            }
        },
        "github": {
            # For each OAuth based provider, either add a ''SocialApp''
            # (''socialaccount'' app) containing the required client
            # credentials, or list them here:
            "APP": {
                "client_id": os.environ.get("GITHUB_CLIENT_ID")
                or config("GITHUB_CLIENT_ID"),
                "secret": os.environ.get("GITHUB_SECRETE") or config("GITHUB_SECRETE"),
                "key": "",
            },
            # For each provider, you can choose whether or not the
            # email address(es) retrieved from the provider are to be
            # interpreted as verified.
            "VERIFIED_EMAIL": True,
        },
    }


# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "django_project.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "django_project.wsgi.application"

# https://docs.djangoproject.com/en/dev/ref/settings/#templates
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

# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DSQL_ENDPOINT = os.environ.get("DSQL_ENDPOINT")
DSQL_CLUSTER_ARN = os.environ.get("DSQL_CLUSTER_ARN")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", "5432")


def get_dsql_auth_token(endpoint: str, cluster_arn: str) -> str:
    client = boto3.client("dsql", region_name=AWS_REGION)
    if hasattr(client, "generate_db_connect_auth_token"):
        return client.generate_db_connect_auth_token(
            Hostname=endpoint,
            Region=AWS_REGION,
            ResourceArn=cluster_arn,
        )
    if hasattr(client, "generate_db_connect_admin_auth_token"):
        return client.generate_db_connect_admin_auth_token(
            Hostname=endpoint,
            Region=AWS_REGION,
            ResourceArn=cluster_arn,
        )
    raise RuntimeError("DSQL auth token generation is not available in boto3.")


if DSQL_ENDPOINT and DSQL_CLUSTER_ARN:
    if not DB_USER:
        raise RuntimeError("DB_USER is required when using DSQL.")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME or "postgres",
            "USER": DB_USER,
            "PASSWORD": get_dsql_auth_token(DSQL_ENDPOINT, DSQL_CLUSTER_ARN),
            "HOST": DSQL_ENDPOINT,
            "PORT": DB_PORT,
        }
    }
    CONN_MAX_AGE = 0
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }

# For Docker/PostgreSQL usage uncomment this and comment the DATABASES config above
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "postgres",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": "db",  # set in docker-compose.yml
#         "PORT": 5432,  # default postgres port
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = "UTC"

# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-USE_I18N
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "staticfiles"

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = AWS_REGION
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [BASE_DIR / "static"]

# https://whitenoise.readthedocs.io/en/latest/django.html
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}

if not AWS_STORAGE_BUCKET_NAME:
    raise RuntimeError("AWS_STORAGE_BUCKET_NAME is required for static storage.")

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-crispy-forms
# https://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "root@localhost"

# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
INTERNAL_IPS = ["127.0.0.1"]

# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = "accounts.CustomUser"

# django-allauth config
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "home"

# https://django-allauth.readthedocs.io/en/latest/views.html#logout-account-logout
ACCOUNT_LOGOUT_REDIRECT_URL = "home"

# https://django-allauth.readthedocs.io/en/latest/installation.html?highlight=backends
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True


# LOG CONFIGURATION

# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO")

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                # exact format is not important, this is the minimum information
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            # console logs to stderr
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            # default for all undefined Python modules
            "": {
                "level": "WARNING",
                "handlers": ["console"],
            },
            # Our application code
            "app": {
                "level": LOGLEVEL,
                "handlers": ["console"],
                # Avoid double logging because of root logger
                "propagate": False,
            },
            # Default runserver request logging
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)


# https://django-taggit.readthedocs.io/en/latest/getting_started.html
TAGGIT_CASE_INSENSITIVE = True
