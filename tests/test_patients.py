import unittest

from services import patients

from exceptions import PatientNotFoundException, PatientsNotAvailableException

from unittest.mock import MagicMock, patch


rid="TEST"

def test_patients_cached_request():
    mock_session_patcher = patch('services.patients.requestsession.doGetJsonRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  (200, {"id": 1, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"})

        status_code, response = patients.getPatientCachedRequest(1)
        assert response["id"] == 1
        assert response["name"] == "Rodrigo"
        assert response["email"] == "rodrigo@gmail.com"
        assert response["phone"] == "(16)998765625"

    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()


def test_patients_existing():
    mock_session_patcher = patch('services.patients.getPatientCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  (200, {"id": 1, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"})

        response = patients.getPatient(rid, 1)
        assert response["id"] == 1
        assert response["name"] == "Rodrigo"
        assert response["email"] == "rodrigo@gmail.com"
        assert response["phone"] == "(16)998765625"

    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()


def test_patients_non_existing():
    mock_session_patcher = patch('services.patients.getPatientCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value = (404, None)
        response = patients.getPatient(rid, 99)
        assert False
    except PatientNotFoundException:
        assert True
    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()


def test_patients_not_available():
    mock_session_patcher = patch('services.patients.getPatientCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = Exception('Error')
        response = patients.getPatient(rid, 1)
        assert False
    except PatientsNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()
