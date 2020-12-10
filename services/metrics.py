import os

from requests.exceptions import Timeout

import logging

from utils import requestsession

from exceptions import MetricsNotAvailableException

logger = logging.getLogger(__name__)

def saveMetrics(clinic, physician, patient):
    #Get config values from env vars
    endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT', 'https://5f71da6964a3720016e60ff8.mockapi.io/v1')
    path = os.getenv('PRESCRIPTIONS_METRICS_PATH', '/metrics')
    bearerToken = os.getenv('PRESCRIPTIONS_METRICS_TOKEN', 'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c')
    timeout = int(os.getenv('PRESCRIPTIONS_METRICS_TIMEOUT', '6'))
    retries = int(os.getenv('PRESCRIPTIONS_METRICS_RETRIES', '5'))
    logger.debug("Metrics service config data: %s", {"endpoint": endpoint, "path": path, "timeout": timeout, "retries": retries})

    try:
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

        logger.debug("Metrics Data: %s", metricsData)

        metricsResponse = None
        logger.debug("Posting metrics to server")
        request = requestsession.getSession(retries)
        request.headers.update({"Content-Type": "application/json"})
        request.headers.update({"Authorization": "Bearer "+bearerToken})
        response = request.post(endpoint+path.format(id=id), timeout=timeout, data=metricsData)
        if(response.status_code == 200):
            metricsResponse = response.json()
            return metricsResponse
        else:
            logger.error("Error trying to access the metrics server: %s", response.text)
            raise MetricsNotAvailableException()
    except:
        raise MetricsNotAvailableException()
