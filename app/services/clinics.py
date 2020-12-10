from cachetools import cached, TTLCache

import os

from utils import requestsession

from requests.exceptions import Timeout

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
clinicCache = TTLCache(maxsize=10000, ttl=259200)


#Config variables
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT')
bearerToken = os.getenv('PRESCRIPTIONS_CLINIC_TOKEN')
timeout = int(os.getenv('PRESCRIPTIONS_CLINIC_TIMEOUT'))
retries = int(os.getenv('PRESCRIPTIONS_CLINIC_RETRIES'))
getClinicPath = os.getenv('PRESCRIPTIONS_CLINIC_PATH')


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