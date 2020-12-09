from cachetools import cached, TTLCache

import os

from requests.exceptions import Timeout

import logging

from utils import requestsession

from exceptions import PhysicianNotFoundException, PhysiciansNotAvailableException

logger = logging.getLogger(__name__)

@cached(cache=TTLCache(maxsize=10000, ttl=172800))
def getPhysician(id):
    #Get config values from env vars
    endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT', 'https://5f71da6964a3720016e60ff8.mockapi.io/v1')
    path = os.getenv('PRESCRIPTIONS_PHYSICIAN_PATH', '/physicians/{id}')
    bearerToken = os.getenv('PRESCRIPTIONS_PHYSICIAN_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA')
    timeout = int(os.getenv('PRESCRIPTIONS_PHYSICIAN_TIMEOUT', '4'))
    retries = int(os.getenv('PRESCRIPTIONS_PHYSICIAN_RETRIES', '2'))
    logger.debug("Physician service config data: %s", {"endpoint": endpoint, "path": path, "timeout": timeout, "retries": retries})

    try:
        physician = None
        logger.debug("Requesting physician data with id %d", id)
        request = requestsession.getSession(retries, bearerToken)
        request.headers.update({"Content-Type": "application/json"})
        request.headers.update({"Authorization": "Bearer "+bearerToken})
        response = request.get(endpoint+path.format(id=id), timeout=timeout)
        if(response.status_code == 200):
            physician = response.json()
            return physician
        else:
            raise PhysicianNotFoundException()
    except PhysicianNotFoundException as exc:
        raise exc
    except:
        raise PhysiciansNotAvailableException()
