import asyncio

from unittest.mock import patch

from services import patients

from exceptions import PatientNotFoundException, PatientsNotAvailableException

from utils import asyncloop


rid="TEST"

def test_patients_request():
    mock_session_patcher = patch('services.patients.requestsession.doGetJsonRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture(
            (200, {"id": 1, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"})
        )

        status_code, response = asyncio.run(patients.getPatientRequest(1))
        assert response["id"] == 1
        assert response["name"] == "Rodrigo"
        assert response["email"] == "rodrigo@gmail.com"
        assert response["phone"] == "(16)998765625"

    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()


def test_patients_existing():
    mock_session_patcher = patch('services.patients.getPatientRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture(
            (200, {"id": 1, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"})
        )

        response = asyncio.run(patients.getPatient(rid, 1))

        assert response["id"] == 1
        assert response["name"] == "Rodrigo"
        assert response["email"] == "rodrigo@gmail.com"
        assert response["phone"] == "(16)998765625"

        #test if cached element is returned, despite of changes in response
        mock_session.return_value =  asyncloop.getTestFuture(
            (200, {"id": 1, "name": "Roberto", "email": "roberto@gmail.com", "phone": "(16)998755625"})
        )
        newresponse = asyncio.run(patients.getPatient(rid, 1))

        assert newresponse["name"] == "Rodrigo"

    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()


def test_patients_non_existing():
    mock_session_patcher = patch('services.patients.getPatientRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value = asyncloop.getTestFuture(
            (404, None)
        )

        asyncio.run(patients.getPatient(rid, 99))
        assert False
    except PatientNotFoundException:
        assert True
    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()


def test_patients_not_available():
    mock_session_patcher = patch('services.patients.getPatientRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = Exception('Error')
        asyncio.run(patients.getPatient(rid, 1))
        assert False
    except PatientsNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()
        patients.clearPatientCache()
