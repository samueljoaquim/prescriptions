from cachetools import cached, TTLCache

import os

import logging

from utils import requestsession

from exceptions import PhysicianNotFoundException, PhysiciansNotAvailableException


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
physicianCache = TTLCache(maxsize=10000, ttl=172800)


#Config variables
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT')
bearerToken = os.getenv('PRESCRIPTIONS_PHYSICIAN_TOKEN')
timeout = int(os.getenv('PRESCRIPTIONS_PHYSICIAN_TIMEOUT'))
retries = int(os.getenv('PRESCRIPTIONS_PHYSICIAN_RETRIES'))
getPhysicianPath = os.getenv('PRESCRIPTIONS_PHYSICIAN_PATH')


async def getPhysician(rid, id):
    try:
        physician = getCached(id)
        if physician is not None:
            logger.debug('%s|Returning cached physician: %s', rid, physician)
            return physician

        logger.debug('%s|Getting physician information for id %d', rid, id)
        status_code, response = await getPhysicianRequest(id)
        if(status_code == 200):
            physician = response
            putInCache(id,physician)
            logger.debug("%s|Physician information: %s", rid, physician)
            return physician
        else:
            raise PhysicianNotFoundException()
    except PhysicianNotFoundException as exc:
        raise exc
    except:
        raise PhysiciansNotAvailableException()


async def getPhysicianRequest(id):
    url = endpoint+getPhysicianPath.format(id=id)
    return await requestsession.doGetJsonRequest(url,retries,timeout,bearerToken)


def getCached(id):
    return physicianCache.get(id)


def putInCache(id,physician):
    physicianCache.setdefault(id,physician)


def clearPhysicianCache():
    physicianCache.clear()
