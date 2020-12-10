import os

from requests.exceptions import Timeout

import logging

from utils import requestsession

from exceptions import MetricsNotAvailableException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


#Config variables
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT', 'https://5f71da6964a3720016e60ff8.mockapi.io/v1')
bearerToken = os.getenv('PRESCRIPTIONS_METRICS_TOKEN', 'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c')
timeout = int(os.getenv('PRESCRIPTIONS_METRICS_TIMEOUT', '6'))
retries = int(os.getenv('PRESCRIPTIONS_METRICS_RETRIES', '5'))
postMetricsPath = os.getenv('PRESCRIPTIONS_METRICS_PATH', '/metrics')


def saveMetrics(rid, metricsData):
    try:
        metricsResponse = None
        status_code, response = saveMetricsRequest(metricsData)
        if(status_code == 200):
            metricsResponse = response
            return metricsResponse
        else:
            raise MetricsNotAvailableException()
    except:
        raise MetricsNotAvailableException()


def saveMetricsRequest(data):
    url = endpoint+postMetricsPath
    return requestsession.doPostJsonRequest(url,data,retries,timeout,bearerToken)
