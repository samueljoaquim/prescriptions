import asyncio

from unittest.mock import patch

from services import physicians

from exceptions import PhysicianNotFoundException, PhysiciansNotAvailableException

from utils import asyncloop


rid="TEST"

def test_physicians_cached_request():
    mock_session_patcher = patch('services.physicians.requestsession.doGetJsonRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture(
            (200, {"id": 1, "name": "José", "crm": "SP293893"})
        )

        status_code, response = asyncio.run(physicians.getPhysicianRequest(1))
        assert response["id"] == 1
        assert response["name"] == "José"
        assert response["crm"] == "SP293893"

    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()

def test_physicians_existing():
    mock_session_patcher = patch('services.physicians.getPhysicianRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture(
            (200, {"id": 1, "name": "José", "crm": "SP293893"})
        )

        response = asyncio.run(physicians.getPhysician(rid, 1))
        assert response["id"] == 1
        assert response["name"] == "José"
        assert response["crm"] == "SP293893"

        #test if cached element is returned, despite of changes in response
        mock_session.return_value =  asyncloop.getTestFuture(
            (200, {"id": 1, "name": "João", "crm": "SP293894"})
        )
        newresponse = asyncio.run(physicians.getPhysician(rid, 1))

        assert newresponse["name"] == "José"
    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()


def test_physicians_non_existing():
    mock_session_patcher = patch('services.physicians.getPhysicianRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  asyncloop.getTestFuture(
            (404, None)
        )

        asyncio.run(physicians.getPhysician(rid, 99))

        assert False

    except PhysicianNotFoundException:
        assert True
    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()


def test_physicians_not_available():
    mock_session_patcher = patch('services.physicians.getPhysicianRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = Exception('Error')
        asyncio.run(physicians.getPhysician(rid, 1))

        assert False
    except PhysiciansNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()
