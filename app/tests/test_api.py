import unittest

import api

from models.validators import validatePrescriptionOutputData, validatePrescriptionErrorMsgData

from flask import json

from exceptions import *

from bson.objectid import ObjectId

from unittest.mock import MagicMock, patch

def test_add_prescription_success():
    requestData = {
        "clinic": {"id": 1},
        "physician": {"id": 1},
        "patient": {"id": 1},
        "text": "validText"
    }

    prescriptionsData = requestData.copy()
    prescriptionsData["_id"] = ObjectId("5fd38feb5a7edab002242277")

    mock_session_patcher = patch('api.prescriptions.savePrescription')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.return_value = prescriptionsData

        client = api.app.test_client()

        ret = client.post('/prescriptions', json=requestData)
        assert ret.status_code == 201

        returnedData = json.loads(ret.data)
        assert returnedData["data"]["clinic"]["id"] == requestData["clinic"]["id"]
        assert returnedData["data"]["physician"]["id"] == requestData["physician"]["id"]
        assert returnedData["data"]["patient"]["id"] == requestData["patient"]["id"]
        assert returnedData["data"]["text"] == requestData["text"]

        assert validatePrescriptionOutputData("TEST", returnedData)

    finally:
        mock_session_patcher.stop()


def test_add_prescription_fail_entity_not_found():
    requestData = {
        "clinic": {"id": 1},
        "physician": {"id": 99},
        "patient": {"id": 1},
        "text": "validText"
    }

    mock_session_patcher = patch('api.prescriptions.savePrescription')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = PhysicianNotFoundException()

        client = api.app.test_client()

        ret = client.post('/prescriptions', json=requestData)
        assert ret.status_code == 404
        
        returnedData = json.loads(ret.data)
        assert returnedData["error"]["code"] == "02"
        assert validatePrescriptionErrorMsgData("TEST", returnedData)

    finally:
        mock_session_patcher.stop()


def test_add_prescription_fail_service_not_available():
    requestData = {
        "clinic": {"id": 1},
        "physician": {"id": 1},
        "patient": {"id": 1},
        "text": "validText"
    }

    mock_session_patcher = patch('api.prescriptions.savePrescription')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = MetricsNotAvailableException()

        client = api.app.test_client()

        ret = client.post('/prescriptions', json=requestData)
        assert ret.status_code == 503
        
        returnedData = json.loads(ret.data)
        assert returnedData["error"]["code"] == "04"
        assert validatePrescriptionErrorMsgData("TEST", returnedData)
    finally:
        mock_session_patcher.stop()


def test_add_prescription_fail_unknown_error():
    requestData = {
        "clinic": {"id": 1},
        "physician": {"id": 1},
        "patient": {"id": 1},
        "text": "validText"
    }

    mock_session_patcher = patch('api.prescriptions.savePrescription')
    mock_session = mock_session_patcher.start()
    try:
        mock_session.side_effect = Exception('error')

        client = api.app.test_client()

        ret = client.post('/prescriptions', json=requestData)
        assert ret.status_code == 500
        
        returnedData = json.loads(ret.data)
        assert returnedData["error"]["code"] == "99"
        assert validatePrescriptionErrorMsgData("TEST", returnedData)
    finally:
        mock_session_patcher.stop()
 