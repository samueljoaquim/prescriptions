import pymongo

import logging

from utils import database

from services import clinics, physicians, patients, metrics

from exceptions import MalformedRequestException

logger = logging.getLogger(__name__)

db = database.getDb()
prescriptionsCol = db.prescriptions


def validatePrescriptionData(prescription):
    return True

def savePrescription(prescription):
    logger.debug('Validating prescription data')
    if not validatePrescriptionData(prescription):
        raise MalformedRequestException()

    logger.debug('Getting clinic information')
    clinic = clinics.getClinic(prescription["clinic"]["id"])
    logger.debug("Clinic information: %s", clinic)

    logger.debug('Getting physician information')
    physician = physicians.getPhysician(prescription["physician"]["id"])
    logger.debug("Physician information: %s", physician)

    logger.debug('Getting patient information')
    patient = patients.getPatient(prescription["patient"]["id"])
    logger.debug("Patient information: %s", patient)

    logger.debug('Saving metrics')
    metricsInfo =metrics.saveMetrics(clinic, physician, patient)
    logger.debug("Metrics information: %s", metricsInfo)

    logger.debug('Saving prescription on the database')
    savedId = prescriptionsCol.insert_one(prescription).inserted_id
    return prescriptionsCol.find_one({"_id": savedId})
