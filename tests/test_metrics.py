import unittest

from services import metrics

from exceptions import MetricsNotAvailableException

from unittest.mock import MagicMock, patch

def test_metrics_success():
    mock_session_patcher = patch('services.metrics.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.post.return_value = MagicMock(status_code=200)
    mock_session.return_value.post.return_value.json.return_value = {
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

    clinic = {"id": 1, "name": "Clínica A"}
    physician = {"id": 1, "name": "José", "crm": "SP293893"}
    patient = {"id": 1, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"}

    response = metrics.saveMetrics(clinic, physician, patient)
    assert response["physician_id"] == 1
    assert response["patient_phone"] == "(16)998765625"
    assert response["clinic_name"] == "Clínica A"
    assert response["physician_crm"] == "SP293893"

    mock_session_patcher.stop()


def test_metrics_not_available():
    mock_session_patcher = patch('services.metrics.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.post.side_effect = Exception('Error')

    clinic = {"id": 2, "name": "Clínica A"}
    physician = {"id": 2, "name": "José", "crm": "SP293893"}
    patient = {"id": 2, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"}

    try:
        response = metrics.saveMetrics(clinic, physician, patient)
        assert False
    except MetricsNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()
