import unittest

from services import clinics

from unittest.mock import MagicMock, patch

def test_clinics_existing():
    mock_session_patcher = patch('services.clinics.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.return_value = MagicMock(status_code=200)
    mock_session.return_value.get.return_value.json.return_value = {"id": 1, "name": "Clínica A"}

    response = clinics.getClinic(1)
    assert response["id"] == 1
    assert response["name"] == "Clínica A"
    mock_session_patcher.stop()
    clinics.clearClinicCache()


def test_clinics_non_existing():
    mock_session_patcher = patch('services.clinics.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.return_value = MagicMock(status_code=404)

    response = clinics.getClinic(99)
    assert response["id"] == 99
    assert "name" not in response
    mock_session_patcher.stop()
    clinics.clearClinicCache()


def test_clinics_not_available():
    mock_session_patcher = patch('services.clinics.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.side_effect = Exception('Error')

    response = clinics.getClinic(2)
    assert response["id"] == 2
