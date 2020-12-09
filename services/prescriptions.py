import pymongo

import logging

import jsonschema

from utils import database

from services import clinics, physicians, patients, metrics

from exceptions import MalformedRequestException

logger = logging.getLogger(__name__)

db = database.getDb()
prescriptionsCol = db.prescriptions

prescriptionsSchema = {
    "type" : "object",
    "properties": {
        "clinic": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"}
            },
            "required": ["id"]
        },
        "physician": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"}
            },
            "required": ["id"]
        },
        "patient": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"}
            },
            "required": ["id"]
        },
        "text": {"type": "string"}
    },
    "required": ["clinic", "physician", "patient", "text"]
}


def validatePrescriptionData(prescription):
    try:
        jsonschema.validate(instance=prescription, schema=prescriptionsSchema)
        return True
    except:
        logger.exception("Error in prescription schema validation")
        return False

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
