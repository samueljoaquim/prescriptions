import unittest

from services import patients

from exceptions import PatientNotFoundException, PatientsNotAvailableException

from unittest.mock import MagicMock, patch

def test_patients_existing():
    mock_session_patcher = patch('services.patients.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.return_value = MagicMock(status_code=200)
    mock_session.return_value.get.return_value.json.return_value = {"id": 1, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"}

    response = patients.getPatient(1)
    assert response["id"] == 1
    assert response["name"] == "Rodrigo"
    assert response["email"] == "rodrigo@gmail.com"
    assert response["phone"] == "(16)998765625"

    mock_session_patcher.stop()
    patients.clearPatientCache()


def test_patients_non_existing():
    mock_session_patcher = patch('services.patients.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.return_value = MagicMock(status_code=404)

    try:
        response = patients.getPatient(99)
        assert False
    except PatientNotFoundException:
        assert True
    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()


def test_patients_not_available():
    mock_session_patcher = patch('services.patients.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.side_effect = Exception('Error')

    try:
        response = patients.getPatient(1)
        assert False
    except PatientsNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()
