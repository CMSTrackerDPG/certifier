from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'testdb',
        'USER': 'postgres',
        'HOST': 'localhost'
    }
}

DYNAMIC_PREFERENCES = {
    'ENABLE_CACHE': False,
}
