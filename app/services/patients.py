from cachetools import cached, TTLCache

import os

import logging

from utils import requestsession

from exceptions import PatientNotFoundException, PatientsNotAvailableException


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
patientCache = TTLCache(maxsize=10000, ttl=43200)


#Config variables
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT')
bearerToken = os.getenv('PRESCRIPTIONS_PATIENT_TOKEN')
timeout = int(os.getenv('PRESCRIPTIONS_PATIENT_TIMEOUT'))
retries = int(os.getenv('PRESCRIPTIONS_PATIENT_RETRIES'))
getPatientPath = os.getenv('PRESCRIPTIONS_PATIENT_PATH')


async def getPatient(rid, id):
    try:
        patient = getCached(id)
        if patient is not None:
            logger.debug('%s|Returning cached patient: %s', rid, patient)
            return patient

        logger.debug('%s|Getting patient information for id %d', rid, id)
        status_code, response = await getPatientRequest(id)
        if(status_code == 200):
            patient = response
            putInCache(id,patient)
            logger.debug("%s|Patient information: %s", rid, patient)
            return patient
        else:
            raise PatientNotFoundException()
    except PatientNotFoundException as exc:
        raise exc
    except:
        raise PatientsNotAvailableException()


async def getPatientRequest(id):
    url = endpoint+getPatientPath.format(id=id)
    return await requestsession.doGetJsonRequest(url,retries,timeout,bearerToken)


def getCached(id):
    return patientCache.get(id)


def putInCache(id,patient):
    patientCache.setdefault(id,patient)


def clearPatientCache():
    patientCache.clear()
    