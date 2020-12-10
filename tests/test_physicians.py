import unittest

from services import physicians

from exceptions import PhysicianNotFoundException, PhysiciansNotAvailableException

from unittest.mock import MagicMock, patch

def test_physicians_existing():
    mock_session_patcher = patch('services.physicians.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.return_value = MagicMock(status_code=200)
    mock_session.return_value.get.return_value.json.return_value = {"id": 1, "name": "José", "crm": "SP293893"}

    response = physicians.getPhysician(1)
    assert response["id"] == 1
    assert response["name"] == "José"
    assert response["crm"] == "SP293893"

    mock_session_patcher.stop()
    physicians.clearPhysicianCache()


def test_physicians_non_existing():
    mock_session_patcher = patch('services.physicians.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.return_value = MagicMock(status_code=404)

    try:
        response = physicians.getPhysician(99)
        assert False
    except PhysicianNotFoundException:
        assert True
    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()


def test_physicians_not_available():
    mock_session_patcher = patch('services.physicians.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    mock_session.return_value = MagicMock()
    mock_session.return_value.get.side_effect = Exception('Error')

    try:
        response = physicians.getPhysician(1)
        assert False
    except PhysiciansNotAvailableException:
        assert True
    except:
        assert False
    finally:
        mock_session_patcher.stop()
        physicians.clearPhysicianCache()
