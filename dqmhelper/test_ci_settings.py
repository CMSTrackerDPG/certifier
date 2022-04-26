from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "127.0.0.1",
        "PASSWORD": "postgres",
        "PORT": 5432,
    }
}

DYNAMIC_PREFERENCES = {
    "ENABLE_CACHE": False,
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("localhost", 6379)],},
    },
}
