import logging

import os

from cachetools import TTLCache

from utils import requestsession


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
clinicCache = TTLCache(maxsize=10000, ttl=259200)


#Config variables
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT')
bearerToken = os.getenv('PRESCRIPTIONS_CLINIC_TOKEN')
timeout = int(os.getenv('PRESCRIPTIONS_CLINIC_TIMEOUT'))
retries = int(os.getenv('PRESCRIPTIONS_CLINIC_RETRIES'))
getClinicPath = os.getenv('PRESCRIPTIONS_CLINIC_PATH')


async def getClinic(rid, id):
    try:
        clinic = getCached(id)
        if clinic is not None:
            logger.debug('%s|Returning cached clinic: %s', rid, clinic)
            return clinic

        clinic = {"id": id}

        logger.debug('%s|Getting clinic information for id %d', rid, id)
        status_code, response = await getClinicRequest(id)
        if status_code == 200:
            clinic = response
            putInCache(id,clinic)
            logger.debug("%s|Clinic information: %s", rid, clinic)
        else:
            logger.warning("%s|Clinic with id %d was not found, returning only default object", rid, id)
    except:
        logger.exception("%s|Error getting clinic, ignoring error", rid)
    return clinic


async def getClinicRequest(id):
    url = endpoint+getClinicPath.format(id=id)
    return await requestsession.doGetJsonRequest(url,retries,timeout,bearerToken)


def getCached(id):
    return clinicCache.get(id)


def putInCache(id,clinic):
    clinicCache.setdefault(id,clinic)


def clearClinicCache():
    clinicCache.clear()
