from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'devcertdb',
        'USER': 'admin',
        'PASSWORD': '',
        'HOST': 'dbod-devcertdb.cern.ch',
        'PORT': '6611'
    }
}

DYNAMIC_PREFERENCES = {
    'ENABLE_CACHE': False,
}
