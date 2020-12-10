import unittest

from services import physicians

from exceptions import PhysicianNotFoundException, PhysiciansNotAvailableException

from unittest.mock import MagicMock, patch


rid="TEST"

def test_physicians_cached_request():
    mock_session_patcher = patch('services.physicians.requestsession.doGetJsonRequest')
    mock_session = mock_session_patcher.start()
    try:    
        mock_session.return_value =  (200, {"id": 1, "name": "José", "crm": "SP293893"})

        status_code, response = physicians.getPhysicianCachedRequest(1)
        assert response["id"] == 1
        assert response["name"] == "José"
        assert response["crm"] == "SP293893"

    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()

def test_physicians_existing():
    mock_session_patcher = patch('services.physicians.getPhysicianCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  (200, {"id": 1, "name": "José", "crm": "SP293893"})

        response = physicians.getPhysician(rid, 1)
        assert response["id"] == 1
        assert response["name"] == "José"
        assert response["crm"] == "SP293893"
    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()


def test_physicians_non_existing():
    mock_session_patcher = patch('services.physicians.getPhysicianCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value =  (404, None)
        response = physicians.getPhysician(rid, 99)
        assert False
    except PhysicianNotFoundException:
        assert True
    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()


def test_physicians_not_available():
    mock_session_patcher = patch('services.physicians.getPhysicianCachedRequest')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = Exception('Error')
        response = physicians.getPhysician(rid, 1)
        assert False
    except PhysiciansNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()
