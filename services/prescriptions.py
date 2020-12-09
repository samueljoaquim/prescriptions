import pymongo

from utils import database

from services import clinics, physicians, patients, metrics

import logging

logger = logging.getLogger(__name__)

db = database.getDb()
prescriptionsCol = db.prescriptions

def savePrescription(prescription):
    logger.debug('Saving prescription')

    logger.debug('Validating clinic')
    clinic = clinics.getClinic(prescription["clinic"]["id"])
    logger.debug('Validating physician')
    physician = physicians.getPhysician(prescription["physician"]["id"])
    logger.debug('validating patient')
    patient = patients.getPatient(prescription["patient"]["id"])

    logger.debug('Saving metrics')
    metrics.saveMetrics(clinic, physician, patient)

    logger.debug('Saving prescription on the database')
    savedId = prescriptionsCol.insert_one(prescription).inserted_id
    return prescriptionsCol.find_one({"_id": savedId})
