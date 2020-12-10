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
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT', 'https://5f71da6964a3720016e60ff8.mockapi.io/v1')
bearerToken = os.getenv('PRESCRIPTIONS_PHYSICIAN_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA')
timeout = int(os.getenv('PRESCRIPTIONS_PHYSICIAN_TIMEOUT', '4'))
retries = int(os.getenv('PRESCRIPTIONS_PHYSICIAN_RETRIES', '2'))
getPhysicianPath = os.getenv('PRESCRIPTIONS_PHYSICIAN_PATH', '/physicians/{id}')


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