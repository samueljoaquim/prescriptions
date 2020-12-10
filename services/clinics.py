from cachetools import cached, TTLCache

import os

from utils import requestsession

from requests.exceptions import Timeout

import logging


logger = logging.getLogger(__name__)
clinicCache = TTLCache(maxsize=10000, ttl=259200)


@cached(clinicCache)
def getClinic(id):
    #Get config values from env vars
    endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT', 'https://5f71da6964a3720016e60ff8.mockapi.io/v1')
    path = os.getenv('PRESCRIPTIONS_CLINIC_PATH', '/clinics/{id}')
    bearerToken = os.getenv('PRESCRIPTIONS_CLINIC_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ')
    timeout = int(os.getenv('PRESCRIPTIONS_CLINIC_TIMEOUT', '5'))
    retries = int(os.getenv('PRESCRIPTIONS_CLINIC_RETRIES', '3'))
    logger.debug("Clinic service config data: %s", {"endpoint": endpoint, "path": path, "timeout": timeout, "retries": retries})

    clinic = {"id": id}
    try:
        logger.debug("Requesting clinic data with id %d", id)
        request = requestsession.getSession(retries)
        request.headers.update({"Content-Type": "application/json"})
        request.headers.update({"Authorization": "Bearer "+bearerToken})
        response = request.get(endpoint+path.format(id=id), timeout=timeout)
        if(response.status_code == 200):
            clinic = response.json()
        else:
            logger.warn("Clinic with id %d was not found, returning only default object", id)
    except:
        logger.exception("Error getting clinic, ignoring error")
    return clinic


def clearClinicCache():
    clinicCache.clear()