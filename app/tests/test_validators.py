from models.validators import *


rid="TEST"

def test_validate_prescriptions_valid():
    assert validatePrescriptionInputData(rid, {
        "clinic": {"id": 123},
        "physician": {"id": 123},
        "patient": {"id": 123},
        "text": "validText"
    })

def test_validate_prescriptions_invalid_text():
    assert not validatePrescriptionInputData(rid, {
        "physician": {"id": 123},
        "patient": {"id": 123}
    })

def test_validate_prescriptions_invalid_clinic():
    assert not validatePrescriptionInputData(rid, {
        "physician": {"id": 123},
        "patient": {"id": 123},
        "text": "validText"
    })
    assert not validatePrescriptionInputData(rid, {
        "clinic": {"noid": 123},
        "physician": {"id": 123},
        "patient": {"id": 123},
        "text": "validText"
    })


def test_validate_prescriptions_invalid_patient():
    assert not validatePrescriptionInputData(rid, {
        "clinic": {"id": 123},
        "physician": {"id": 123},
        "text": "validText"
    })
    assert not validatePrescriptionInputData(rid, {
        "clinic": {"id": 123},
        "physician": {"id": 123},
        "patient": {"noid": 123},
        "text": "validText"
    })


def test_validate_prescriptions_invalid_physician():
    assert not validatePrescriptionInputData(rid, {
        "clinic": {"id": 123},
        "patient": {"id": 123},
        "text": "validText"
    })
    assert not validatePrescriptionInputData(rid, {
        "clinic": {"id": 123},
        "physician": {"noid": 123},
        "patient": {"id": 123},
        "text": "validText"
    })


def test_validate_prescriptions_output_valid():
    assert validatePrescriptionOutputData(rid, {
        "data": {
            "id": {"$oid": "5fd38feb5a7edab002242277"},
            "clinic": {"id": 2},
            "physician": {"id": 3},
            "patient": {"id": 2},
            "text": "Dipirona 1x ao dia"
        }
    })


def test_validate_prescriptions_output_invalid_physician():
    assert not validatePrescriptionOutputData(rid, {
        "data": {
            "id": {"$oid": "5fd38feb5a7edab002242277"},
            "clinic": {"id": 2},
            "patient": {"id": 2},
            "text": "Dipirona 1x ao dia"
        }
    })


def test_validate_prescriptions_output_invalid_id():
    assert not validatePrescriptionOutputData(rid, {
        "data": {
            "clinic": {"id": 2},
            "physician": {"id": 3},
            "patient": {"id": 2},
            "text": "Dipirona 1x ao dia"
        }
    })


def test_validate_prescriptions_error_msg():
    assert validatePrescriptionErrorMsgData(rid, {
      "error": {
        "message": "patient not found",
        "code": "03"
      }
    })


def test_validate_prescriptions_error_msg_invalid():
    assert not validatePrescriptionErrorMsgData(rid, {
      "error": {
        "message": "patient not found",
      }
    })


