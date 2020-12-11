import unittest

from services import prescriptions

from exceptions import MalformedRequestException

from unittest.mock import MagicMock, patch

from utils import asyncloop


rid="TEST"

def test_validate_prescriptions_valid():
    assert prescriptions.validatePrescriptionData(rid, {
        "clinic": {"id": 123},
        "physician": {"id": 123},
        "patient": {"id": 123},
        "text": "validText"
    })

def test_validate_prescriptions_invalid_text():
    assert not prescriptions.validatePrescriptionData(rid, {
        "physician": {"id": 123},
        "patient": {"id": 123}
    })

def test_validate_prescriptions_invalid_clinic():
    assert not prescriptions.validatePrescriptionData(rid, {
        "physician": {"id": 123},
        "patient": {"id": 123},
        "text": "validText"
    })
    assert not prescriptions.validatePrescriptionData(rid, {
        "clinic": {"noid": 123},
        "physician": {"id": 123},
        "patient": {"id": 123},
        "text": "validText"
    })


def test_validate_prescriptions_invalid_patient():
    assert not prescriptions.validatePrescriptionData(rid, {
        "clinic": {"id": 123},
        "physician": {"id": 123},
        "text": "validText"
    })
    assert not prescriptions.validatePrescriptionData(rid, {
        "clinic": {"id": 123},
        "physician": {"id": 123},
        "patient": {"noid": 123},
        "text": "validText"
    })


def test_validate_prescriptions_invalid_physician():
    assert not prescriptions.validatePrescriptionData(rid, {
        "clinic": {"id": 123},
        "patient": {"id": 123},
        "text": "validText"
    })
    assert not prescriptions.validatePrescriptionData(rid, {
        "clinic": {"id": 123},
        "physician": {"noid": 123},
        "patient": {"id": 123},
        "text": "validText"
    })


def test_save_prescription_with_invalid_data():
    try:
        prescriptions.savePrescription(rid, {
            "physician": {"id": 1},
            "patient": {"id": 1},
            "text": "validText"
        })
        assert True
    except MalformedRequestException:
        assert True
    except:
        assert False


def test_save_prescription_with_clinic_name():
    metricsData = {
          "clinic_id": 1,
          "clinic_name": "Clínica A",
          "physician_id": 1,
          "physician_name": "José",
          "physician_crm": "SP293893",
          "patient_id": 1,
          "patient_name": "Rodrigo",
          "patient_email": "rodrigo@gmail.com",
          "patient_phone": "(16)998765625"
    }

    mock_clinics_patcher = patch('services.prescriptions.clinics')
    mock_clinics = mock_clinics_patcher.start()
    async def getClinicFuture(a, b):
        return {"id": 1, "name": "Clínica A"}

    mock_clinics.getClinic = getClinicFuture

    mock_physicians_patcher = patch('services.prescriptions.physicians')
    mock_physicians = mock_physicians_patcher.start()
    async def getPhysicianFuture(a, b):
        return {"id": 1, "name": "José", "crm": "SP293893"}

    mock_physicians.getPhysician = getPhysicianFuture

    mock_patients_patcher = patch('services.prescriptions.patients')
    mock_patients = mock_patients_patcher.start()
    async def getPatientFuture(a, b):
        return {"id": 1, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"}

    mock_patients.getPatient = getPatientFuture


    mock_metrics_patcher = patch('services.prescriptions.metrics')
    mock_metrics = mock_metrics_patcher.start()
    async def saveMetricsFuture(a, b):
        return metricsData

    mock_metrics.saveMetrics = saveMetricsFuture


    mock_database_patcher = patch('services.prescriptions.database.getDb')
    mock_database = mock_database_patcher.start()
    mock_database.return_value = MagicMock()
    mock_database.return_value.prescriptions = MagicMock()
    mock_database.return_value.prescriptions.prescriptions = MagicMock()
    mock_database.return_value.prescriptions.prescriptions.insert_one.return_value = MagicMock(inserted_id=1)
    response = metricsData.copy()
    response["_id"] = 1
    mock_database.return_value.prescriptions.prescriptions.find_one.return_value = response

    try:
        element = prescriptions.savePrescription(rid, {
            "clinic": {"id": 1},
            "physician": {"id": 1},
            "patient": {"id": 1},
            "text": "validText"
        })
        assert element["_id"] == 1
    finally:
        mock_clinics_patcher.stop()
        mock_physicians_patcher.stop()
        mock_patients_patcher.stop()
        mock_metrics_patcher.stop()
        mock_database_patcher.stop()



def test_save_prescription_without_clinic_name():
    metricsData = {
          "clinic_id": 1,
          "physician_id": 1,
          "physician_name": "José",
          "physician_crm": "SP293893",
          "patient_id": 1,
          "patient_name": "Rodrigo",
          "patient_email": "rodrigo@gmail.com",
          "patient_phone": "(16)998765625"
    }

    mock_clinics_patcher = patch('services.prescriptions.clinics')
    mock_clinics = mock_clinics_patcher.start()
    async def getClinicFuture(a, b):
        return {"id": 1}

    mock_clinics.getClinic = getClinicFuture

    mock_physicians_patcher = patch('services.prescriptions.physicians')
    mock_physicians = mock_physicians_patcher.start()
    async def getPhysicianFuture(a, b):
        return {"id": 1, "name": "José", "crm": "SP293893"}

    mock_physicians.getPhysician = getPhysicianFuture

    mock_patients_patcher = patch('services.prescriptions.patients')
    mock_patients = mock_patients_patcher.start()
    async def getPatientFuture(a, b):
        return {"id": 1, "name": "Rodrigo", "email": "rodrigo@gmail.com", "phone": "(16)998765625"}

    mock_patients.getPatient = getPatientFuture


    mock_metrics_patcher = patch('services.prescriptions.metrics')
    mock_metrics = mock_metrics_patcher.start()
    async def saveMetricsFuture(a, b):
        return metricsData

    mock_metrics.saveMetrics = saveMetricsFuture


    mock_database_patcher = patch('services.prescriptions.database.getDb')
    mock_database = mock_database_patcher.start()
    mock_database.return_value = MagicMock()
    mock_database.return_value.prescriptions = MagicMock()
    mock_database.return_value.prescriptions.prescriptions = MagicMock()
    mock_database.return_value.prescriptions.prescriptions.insert_one.return_value = MagicMock(inserted_id=1)
    response = metricsData.copy()
    response["_id"] = 1
    mock_database.return_value.prescriptions.prescriptions.find_one.return_value = response

    try:
        element = prescriptions.savePrescription(rid, {
            "clinic": {"id": 1},
            "physician": {"id": 1},
            "patient": {"id": 1},
            "text": "validText"
        })
        print(element)
        assert element["_id"] == 1
    finally:
        mock_clinics_patcher.stop()
        mock_physicians_patcher.stop()
        mock_patients_patcher.stop()
        mock_metrics_patcher.stop()
        mock_database_patcher.stop()
