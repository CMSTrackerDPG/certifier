from .settings import *

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres-local",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "PORT": "5432"
            # 'HOST': 'localhost'
        }
    }

DYNAMIC_PREFERENCES = {
    "ENABLE_CACHE": False,
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
