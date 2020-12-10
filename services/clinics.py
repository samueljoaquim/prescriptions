from cachetools import cached, TTLCache

import os

from utils import requestsession

from requests.exceptions import Timeout

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
clinicCache = TTLCache(maxsize=10000, ttl=259200)


#Config variables
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT', 'https://5f71da6964a3720016e60ff8.mockapi.io/v1')
bearerToken = os.getenv('PRESCRIPTIONS_CLINIC_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ')
timeout = int(os.getenv('PRESCRIPTIONS_CLINIC_TIMEOUT', '5'))
retries = int(os.getenv('PRESCRIPTIONS_CLINIC_RETRIES', '3'))
getClinicPath = os.getenv('PRESCRIPTIONS_CLINIC_PATH', '/clinics/{id}')


def getClinic(rid, id):
    clinic = {"id": id}
    try:
        status_code, response = getClinicCachedRequest(id)
        if(status_code == 200):
            clinic = response
        else:
            logger.warn("%s|Clinic with id %d was not found, returning only default object", rid, id)
    except:
        logger.exception("%s|Error getting clinic, ignoring error", rid)
    return clinic


@cached(clinicCache)
def getClinicCachedRequest(id):
    url = endpoint+getClinicPath.format(id=id)
    return requestsession.doGetJsonRequest(url,retries,timeout,bearerToken)


def clearClinicCache():
    clinicCache.clear()