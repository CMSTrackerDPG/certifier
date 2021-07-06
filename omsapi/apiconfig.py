from decouple import config

API_URL = 'https://vocms0185.cern.ch/agg/api'
API_VERSION = 'v1'
API_AUDIENCE = 'cmsoms-int-0185'
OMS_CLIENT_ID = config('OMS_CLIENT_ID')
OMS_CLIENT_SECRET = config('OMS_CLIENT_SECRET')
