from omsapi.api import OMSAPI
from omsapi.apiconfig import API_URL, API_VERSION, API_AUDIENCE, OMS_CLIENT_ID, OMS_CLIENT_SECRET

### set names of filter attributes

def get_oms_api():
    '''
    These parameters can be changed in the file apiconfig.py
    '''
    omsapi = OMSAPI(api_url=API_URL, api_version=API_VERSION, cert_verify=False)
    omsapi.auth_oidc(OMS_CLIENT_ID, OMS_CLIENT_SECRET, audience=API_AUDIENCE)
    return omsapi

def get_oms_fill(fill_number):
    omsapi = get_oms_api()
    oms_query = omsapi.query("fills")
    oms_query.filter("fill_number", fill_number)
    response = oms_query.data().json()
    if response['data']:
        return response['data'][0]
    else:
        return None  
        
def get_oms_run(run_number):
    omsapi = get_oms_api()
    oms_query = omsapi.query("runs")
    oms_query.filter("run_number", run_number)
    response = oms_query.data().json()
    if response['data']:
        return response['data'][0]
    else:
        return None

def get_oms_lumisection_count(run_number):
    omsapi = get_oms_api()
    oms_query = omsapi.query("lumisections")
    oms_query.filter("run_number", run_number).sort("lumisection_number", asc=False)
    oms_query.paginate(per_page = 1)
    response = oms_query.data().json()
    if response['data']:
        return response['data'][0]['attributes']['lumisection_number']
    else:
        return 0

  