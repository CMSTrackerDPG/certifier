"""
Django settings for dqmhelper project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from pathlib import Path

from decouple import config
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}
# Version to display in order to keep track of changes
CERTHELPER_VERSION = "1.8.1"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")
DJANGO_SECRET_ACC = config("DJANGO_SECRET_ACC", default="admin")
DJANGO_SECRET_PASS = config("DJANGO_SECRET_PASS", default="admin")

# Redis Server Hostname
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PASSWORD = config("REDIS_PASSWORD", default="")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    config("DJANGO_ALLOWED_HOSTS", default="localhost"),
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [config("CSRF_TRUSTED_ORIGINS", default="")]

INSTALLED_APPS = [
    "channels",
    "remotescripts",
    "openruns.apps.OpenrunsConfig",
    "addrefrun.apps.AddrefrunConfig",
    "summary.apps.SummaryConfig",
    "restore.apps.RestoreConfig",
    "delete.apps.DeleteConfig",
    "shiftleader.apps.ShiftleaderConfig",
    "tables.apps.TablesConfig",
    "listruns.apps.ListrunsConfig",
    "checklists.apps.ChecklistsConfig",
    "users.apps.UsersConfig",
    "home.apps.HomeConfig",
    "certifier.apps.CertifierConfig",
    "oms.apps.OmsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "bootstrap3",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.cern",
    "allauth.socialaccount.providers.github",
    "widget_tweaks",
    "django_extensions",
    "django_tables2",
    "django_filters",
    "ckeditor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dqmhelper.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dqmhelper.context_processors.global_context",
            ]
        },
    }
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = "/"

# WSGI_APPLICATION = "dqmhelper.wsgi.application"
ASGI_APPLICATION = "dqmhelper.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis://:" + REDIS_PASSWORD + "@" + REDIS_HOST + ":6379/0")],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DJANGO_DATABASE_ENGINE", default=""),
        "NAME": config("DJANGO_DATABASE_NAME", default=""),
        "USER": config("DJANGO_DATABASE_USER", default=""),
        "PASSWORD": config("DJANGO_DATABASE_PASSWORD", default=""),
        "HOST": config("DJANGO_DATABASE_HOST", default=""),
        "PORT": config("DJANGO_DATABASE_PORT", default=""),
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 2

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "WARNING",
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} - {asctime} - {module} - {message}",
            "style": "{",
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (
    BASE_DIR / "home" / "static",
    BASE_DIR / "checklists" / "static",
    BASE_DIR / "listruns" / "static",
)
# STATIC_ROOT = os.path.join(BASE_DIR, 'wsgi/static')
STATIC_ROOT = BASE_DIR / "sock" / "asgi" / "static"

AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("DJANGO_EMAIL_HOST", default="localhost")
EMAIL_PORT = config("DJANGO_EMAIL_PORT", default=25, cast=int)
EMAIL_HOST_USER = config("DJANGO_EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("DJANGO_EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("DJANGO_EMAIL_USE_TLS", default=False, cast=bool)
SERVER_EMAIL = config("DJANGO_SERVER_EMAIL", default="root@localhost")

CERN_CERTIFICATE_PATH = config("CERN_CERTIFICATE_PATH", default="")

# When Upgraded to Django 3.2 - RELEASE 06.04.2021
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
