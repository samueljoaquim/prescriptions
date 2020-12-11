import os

import logging

from utils import requestsession

from exceptions import MetricsNotAvailableException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


#Config variables
endpoint = os.getenv('PRESCRIPTIONS_ENDPOINT')
bearerToken = os.getenv('PRESCRIPTIONS_METRICS_TOKEN')
timeout = int(os.getenv('PRESCRIPTIONS_METRICS_TIMEOUT'))
retries = int(os.getenv('PRESCRIPTIONS_METRICS_RETRIES'))
postMetricsPath = os.getenv('PRESCRIPTIONS_METRICS_PATH')


async def saveMetrics(rid, metricsData):
    try:
        metricsResponse = None
        status_code, response = await saveMetricsRequest(metricsData)
        if(status_code == 201):
            metricsResponse = response
            return metricsResponse
        else:
            raise MetricsNotAvailableException()
    except:
        raise MetricsNotAvailableException()


async def saveMetricsRequest(data):
    url = endpoint+postMetricsPath
    return await requestsession.doPostJsonRequest(url,data,retries,timeout,bearerToken)
