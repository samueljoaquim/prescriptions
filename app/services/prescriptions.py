import logging

import asyncio

from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, AutoReconnect

from utils import asyncloop, database

from services import clinics, physicians, patients, metrics

from exceptions import DatabaseNotAvailableException


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
    loop = asyncloop.getOrCreateEventloop()

    logger.debug('%s|Running requests for clinic, physician and patient',rid)
    responses = loop.run_until_complete(asyncio.gather(
        clinics.getClinic(rid, prescription["clinic"]["id"]),
        physicians.getPhysician(rid, prescription["physician"]["id"]),
        patients.getPatient(rid, prescription["patient"]["id"])
    ))
    logger.debug('%s|Responses: %s',rid, responses)
    clinic = responses[0]
    physician = responses[1]
    patient = responses[2]

    logger.debug('%s|Saving metrics', rid)
    metricsData = assembleMetricsData(rid, clinic, physician, patient)
    logger.debug("%s|Metrics request data: %s", rid, metricsData)
    metricsInfo = asyncio.run(metrics.saveMetrics(rid, metricsData))
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
