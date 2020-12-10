from cachetools import cached, TTLCache

import os

from requests.exceptions import Timeout

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


def getPhysician(rid, id):
    try:
        physician = None
        status_code, response = getPhysicianCachedRequest(id)
        if(status_code == 200):
            physician = response
            return physician
        else:
            raise PhysicianNotFoundException()
    except PhysicianNotFoundException as exc:
        raise exc
    except:
        raise PhysiciansNotAvailableException()


@cached(physicianCache)
def getPhysicianCachedRequest(id):
    url = endpoint+getPhysicianPath.format(id=id)
    return requestsession.doGetJsonRequest(url,retries,timeout,bearerToken)


def clearPhysicianCache():
    physicianCache.clear()