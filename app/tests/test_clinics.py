import asyncio

from unittest.mock import patch

from services import clinics

from utils import asyncloop


rid = "TEST"

def test_clinics_request():
    mock_session_patcher = patch('services.clinics.requestsession.doGetJsonRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture((200, {"id": 1, "name": "Clínica A"}))

        status_code, response = asyncio.run(clinics.getClinicRequest(1))
        assert response["id"] == 1
        assert response["name"] == "Clínica A"
    finally:
        mock_session_patcher.stop()
        clinics.clearClinicCache()


def test_clinics_existing():
    mock_session_patcher = patch('services.clinics.getClinicRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture((200, {"id": 1, "name": "Clínica A"}))

        response = asyncio.run(clinics.getClinic(rid,1))

        assert response["id"] == 1
        assert response["name"] == "Clínica A"

        #test if cached element is returned, despite of changes in response
        mock_session.return_value =  asyncloop.getTestFuture((200, {"id": 1, "name": "Clínica B"}))
        newresponse = asyncio.run(clinics.getClinic(rid,1))

        assert newresponse["name"] == "Clínica A"

    finally:
        mock_session_patcher.stop()
        clinics.clearClinicCache()


def test_clinics_non_existing():
    mock_session_patcher = patch('services.clinics.getClinicRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture((404, None))

        response = asyncio.run(clinics.getClinic(rid,99))
        assert response["id"] == 99
        assert "name" not in response
    finally:
        mock_session_patcher.stop()
        clinics.clearClinicCache()


def test_clinics_not_available():
    mock_session_patcher = patch('services.clinics.getClinicRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = Exception('Error')

        response = asyncio.run(clinics.getClinic(rid,2))
        assert response["id"] == 2
    finally:
        mock_session_patcher.stop()
        clinics.clearClinicCache()
