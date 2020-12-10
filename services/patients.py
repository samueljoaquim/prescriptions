from cachetools import cached, TTLCache

import os

from requests.exceptions import Timeout

import logging

from utils import requestsession

from exceptions import PatientNotFoundException, PatientsNotAvailableException


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
patientCache = TTLCache(maxsize=10000, ttl=43200)


#Config variables
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT', 'https://5f71da6964a3720016e60ff8.mockapi.io/v1')
bearerToken = os.getenv('PRESCRIPTIONS_PATIENT_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU')
timeout = int(os.getenv('PRESCRIPTIONS_PATIENT_TIMEOUT', '3'))
retries = int(os.getenv('PRESCRIPTIONS_PATIENT_RETRIES', '2'))
getPatientPath = os.getenv('PRESCRIPTIONS_PATIENT_PATH', '/patients/{id}')


def getPatient(rid, id):
    try:
        patient = None
        status_code, response = getPatientCachedRequest(id)
        if(status_code == 200):
            patient = response
            return patient
        else:
            raise PatientNotFoundException()
    except PatientNotFoundException as exc:
        raise exc
    except:
        raise PatientsNotAvailableException()


@cached(patientCache)
def getPatientCachedRequest(id):
    url = endpoint+getPatientPath.format(id=id)
    return requestsession.doGetJsonRequest(url,retries,timeout,bearerToken)


def clearPatientCache():
    patientCache.clear()