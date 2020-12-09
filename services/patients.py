from cachetools import cached, TTLCache

import os

from requests.exceptions import Timeout

import logging

from utils import requestsession

from exceptions import PatientNotFoundException, PatientsNotAvailableException

logger = logging.getLogger(__name__)

@cached(cache=TTLCache(maxsize=10000, ttl=43200))
def getPatient(id):
    #Get config values from env vars
    endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT', 'https://5f71da6964a3720016e60ff8.mockapi.io/v1')
    path = os.getenv('PRESCRIPTIONS_PATIENT_PATH', '/patients/{id}')
    bearerToken = os.getenv('PRESCRIPTIONS_PATIENT_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU')
    timeout = int(os.getenv('PRESCRIPTIONS_PATIENT_TIMEOUT', '3'))
    retries = int(os.getenv('PRESCRIPTIONS_PATIENT_RETRIES', '2'))
    logger.debug("Patient service config data: %s", {"endpoint": endpoint, "path": path, "timeout": timeout, "retries": retries})

    try:
        patient = None
        logger.debug("Requesting patient data with id %d", id)
        request = requestsession.getSession(retries, bearerToken)
        request.headers.update({"Content-Type": "application/json"})
        request.headers.update({"Authorization": "Bearer "+bearerToken})
        response = request.get(endpoint+path.format(id=id), timeout=timeout)
        if(response.status_code == 200):
            patient = response.json()
            return patient
        else:
            raise PatientNotFoundException()
    except PatientNotFoundException as exc:
        raise exc
    except:
        raise PatientsNotAvailableException()
