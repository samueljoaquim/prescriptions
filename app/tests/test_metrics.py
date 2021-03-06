import asyncio

from unittest.mock import patch

from services import metrics

from exceptions import MetricsNotAvailableException

from utils import asyncloop


rid="TEST"

def test_clinics_save_request():
    metricsData = {
      "clinic_id": 1,
      "clinic_name": "Clínica A",
      "physician_id": 1,
      "physician_name": "José",
      "physician_crm": "SP293893",
      "patient_id": 1,
      "patient_name": "Rodrigo",
      "patient_email": "rodrigo@gmail.com",
      "patient_phone": "(16)998765625"
    }

    mock_session_patcher = patch('services.metrics.requestsession.doPostJsonRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture((201, metricsData))

        status_code, response = asyncio.run(metrics.saveMetricsRequest(metricsData))
        assert response["physician_id"] == 1
        assert response["patient_phone"] == "(16)998765625"
        assert response["clinic_name"] == "Clínica A"
        assert response["physician_crm"] == "SP293893"
    finally:
        mock_session_patcher.stop()


def test_metrics_success():
    metricsData = {
      "clinic_id": 1,
      "clinic_name": "Clínica A",
      "physician_id": 1,
      "physician_name": "José",
      "physician_crm": "SP293893",
      "patient_id": 1,
      "patient_name": "Rodrigo",
      "patient_email": "rodrigo@gmail.com",
      "patient_phone": "(16)998765625"
    }

    mock_session_patcher = patch('services.metrics.saveMetricsRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture((201, metricsData))

        response = asyncio.run(metrics.saveMetrics(rid, metricsData))
        assert response["physician_id"] == 1
        assert response["patient_phone"] == "(16)998765625"
        assert response["clinic_name"] == "Clínica A"
        assert response["physician_crm"] == "SP293893"
    finally:
        mock_session_patcher.stop()


def test_metrics_error_status():
    metricsData = {
      "clinic_id": 2,
      "clinic_name": "Clínica B",
      "physician_id": 2,
      "physician_name": "John",
      "physician_crm": "SP293894",
      "patient_id": 2,
      "patient_name": "Roberto",
      "patient_email": "roberto@gmail.com",
      "patient_phone": "(16)998765623"
    }

    mock_session_patcher = patch('services.metrics.saveMetricsRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture((500, None))
        asyncio.run(metrics.saveMetrics(rid, metricsData))
        assert False
    except MetricsNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()


def test_metrics_exception():
    metricsData = {
      "clinic_id": 2,
      "clinic_name": "Clínica B",
      "physician_id": 2,
      "physician_name": "John",
      "physician_crm": "SP293894",
      "patient_id": 2,
      "patient_name": "Roberto",
      "patient_email": "roberto@gmail.com",
      "patient_phone": "(16)998765623"
    }

    mock_session_patcher = patch('services.metrics.saveMetricsRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = Exception('Error')
        asyncio.run(metrics.saveMetrics(rid, metricsData))
        assert False
    except MetricsNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()
