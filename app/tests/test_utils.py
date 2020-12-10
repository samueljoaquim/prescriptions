import unittest

from utils import requestsession

from unittest.mock import MagicMock, patch


def test_get_json_request_ok():
    mock_session_patcher = patch('utils.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value = MagicMock()
        mock_session.return_value.get.return_value = MagicMock(status_code=200)
        mock_session.return_value.get.return_value.json.return_value = {"id": 1, "name": "Clínica A"}

        status_code, response = requestsession.doGetJsonRequest("url",1,1,"abc")
        assert response["id"] == 1
        assert response["name"] == "Clínica A"
    finally:
        mock_session_patcher.stop()


def test_get_json_request_nok():
    mock_session_patcher = patch('utils.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value = MagicMock()
        mock_session.return_value.get.return_value = MagicMock(status_code=404)
        mock_session.return_value.get.return_value.json.return_value = None

        status_code, response = requestsession.doGetJsonRequest("url",1,1,"abc")
        assert status_code == 404
    finally:
        mock_session_patcher.stop()


def test_post_json_request_ok():
    mock_session_patcher = patch('utils.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value = MagicMock()
        mock_session.return_value.post.return_value = MagicMock(status_code=200)
        mock_session.return_value.post.return_value.json.return_value = {"id": 1, "name": "Clínica A"}

        status_code, response = requestsession.doPostJsonRequest("url",{},1,1,"abc")
        assert response["id"] == 1
        assert response["name"] == "Clínica A"
    finally:
        mock_session_patcher.stop()


def test_post_json_request_nok():
    mock_session_patcher = patch('utils.requestsession.getSession')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value = MagicMock()
        mock_session.return_value.post.return_value = MagicMock(status_code=404)
        mock_session.return_value.post.return_value.json.return_value = None

        status_code, response = requestsession.doPostJsonRequest("url",{},1,1,"abc")
        assert status_code == 404
    finally:
        mock_session_patcher.stop()
