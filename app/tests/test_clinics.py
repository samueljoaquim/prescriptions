import unittest

from services import clinics

from unittest.mock import MagicMock, patch


rid = "TEST"

def test_clinics_cached_request():
    mock_session_patcher = patch('services.clinics.requestsession.doGetJsonRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  (200, {"id": 1, "name": "Clínica A"})

        status_code, response = clinics.getClinicCachedRequest(1)
        assert response["id"] == 1
        assert response["name"] == "Clínica A"
    finally:
        mock_session_patcher.stop()
        clinics.clearClinicCache()


def test_clinics_existing():
    mock_session_patcher = patch('services.clinics.getClinicCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  (200, {"id": 1, "name": "Clínica A"})

        response = clinics.getClinic(rid,1)
        assert response["id"] == 1
        assert response["name"] == "Clínica A"
    finally:
        mock_session_patcher.stop()
        clinics.clearClinicCache()


def test_clinics_non_existing():
    mock_session_patcher = patch('services.clinics.getClinicCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  (404, None)

        response = clinics.getClinic(rid,99)
        assert response["id"] == 99
        assert "name" not in response
    finally:
        mock_session_patcher.stop()
        clinics.clearClinicCache()


def test_clinics_not_available():
    mock_session_patcher = patch('services.clinics.getClinicCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = Exception('Error')

        response = clinics.getClinic(rid,2)
        assert response["id"] == 2
    finally:
        mock_session_patcher.stop()
        clinics.clearClinicCache()
