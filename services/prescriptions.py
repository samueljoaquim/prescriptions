import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, AutoReconnect

import logging

import jsonschema

from utils import database

from services import clinics, physicians, patients, metrics

from models.schemas import prescriptionsSchema

from exceptions import MalformedRequestException, DatabaseNotAvailableException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def validatePrescriptionData(rid, prescription):
    try:
        jsonschema.validate(instance=prescription, schema=prescriptionsSchema)
        return True
    except:
        logger.exception("%s|Error in prescription schema validation", rid)
        return False


def assembleMetricsData(rid, clinic, physician, patient):
    metricsData = {
          "clinic_id": clinic["id"],
          "physician_id": physician["id"],
          "physician_name": physician["name"],
          "physician_crm": physician["crm"],
          "patient_id": patient["id"],
          "patient_name": patient["name"],
          "patient_email": patient["email"],
          "patient_phone": patient["phone"]
    }
    if "name" in clinic:
          metricsData["clinic_name"] = clinic["name"]

    logger.debug("%s|Metrics Data: %s", rid, metricsData)
    return metricsData


def savePrescription(rid, prescription):
    logger.debug('%s|Validating prescription data',rid)
    if not validatePrescriptionData(rid, prescription):
        raise MalformedRequestException()

    logger.debug('%s|Getting clinic information for id %d', rid, prescription["clinic"]["id"])
    clinic = clinics.getClinic(rid, prescription["clinic"]["id"])
    logger.debug("%s|Clinic information: %s", rid, clinic)

    logger.debug('%s|Getting physician information for id %d', rid, prescription["physician"]["id"])
    physician = physicians.getPhysician(rid, prescription["physician"]["id"])
    logger.debug("%s|Physician information: %s", rid, physician)

    logger.debug('%s|Getting patient information for id %d', rid, prescription["patient"]["id"])
    patient = patients.getPatient(rid, prescription["patient"]["id"])
    logger.debug("%s|Patient information: %s", rid, patient)

    logger.debug('%s|Saving metrics', rid)
    metricsData = assembleMetricsData(rid, clinic, physician, patient)
    logger.debug("%s|Metrics request data: %s", rid, metricsData)
    metricsInfo =metrics.saveMetrics(rid, metricsData)
    logger.debug("%s|Metrics returned information: %s", rid, metricsInfo)

    logger.debug('%s|Saving prescription on the database', rid)
    try:
        db = database.getDb()
        prescriptionsCol = db.prescriptions.prescriptions
        savedId = prescriptionsCol.insert_one(prescription).inserted_id
        return prescriptionsCol.find_one({"_id": savedId})
    except (ConnectionFailure, ServerSelectionTimeoutError, AutoReconnect):
        raise DatabaseNotAvailableException()
    finally:
        try:
            db.close()
        except:
            pass

