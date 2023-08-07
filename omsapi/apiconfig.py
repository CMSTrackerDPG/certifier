from decouple import config

# See other options here:
# https://gitlab.cern.ch/cmsoms/oms-api-client/-/wikis/uploads/01fe5b10560e76849ce636cf53e59e20/OMS_CERN_OpenID_API__2022_.pdf
API_URL = config("OMS_API_URL", "https://cmsoms.cern.ch/agg/api")
API_VERSION = "v1"
API_AUDIENCE = config("OMS_API_AUDIENCE", "cmsoms-prod")
OMS_CLIENT_ID = config("OMS_CLIENT_ID")
OMS_CLIENT_SECRET = config("OMS_CLIENT_SECRET")
