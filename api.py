from bson.json_util import dumps
import pymongo

from cachetools import cached, TTLCache

import flask
from flask import request


app = flask.Flask(__name__)
app.config['DEBUG'] = True


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.prescriptions
prescriptionsDb = db.prescriptions

#[POST] - /prescriptions
#  Validate clinic, physician and patient ids, save metrics and
#  return the prescription request data with and added id
#
#  Request body example:
#  {
#   "clinic": {
#     "id": 1
#   },
#   "physician": {
#     "id": 1
#   },
#   "patient": {
#     "id": 1
#   },
#   "text": "Dipirona 1x ao dia"
#  }
#
#  Response body example:
# {
#   "data": {
#     "id": 1,
#     "clinic": {
#       "id": 1
#     },
#     "physician": {
#       "id": 1
#     },
#     "patient": {
#       "id": 1
#     },
#     "text": "Dipirona 1x ao dia"
#   }
# }
@app.route('/prescriptions', methods=['POST'])
def savePrescription():
    prescriptionData = request.json

    clinic = getClinic(prescriptionData["clinic"]["id"])
    physician = getPhysician(prescriptionData["physician"]["id"])
    patient = getPatient(prescriptionData["patient"]["id"])

    saveMetrics(clinic, physician, patient)

    entry = savePrescription(prescriptionData)

    return dumps({"data": entry})


@cached(cache=TTLCache(maxsize=10000, ttl=259200))
def getClinic(id):
    return id


@cached(cache=TTLCache(maxsize=10000, ttl=172800))
def getPhysician(id):
    return id


@cached(cache=TTLCache(maxsize=10000, ttl=43200))
def getPatient(id):
    return id


def saveMetrics(clinic, physician, patient):
    pass


def savePrescription(prescription):
    savedId = prescriptionsDb.insert_one(prescription).inserted_id
    return prescriptionsDb.find_one({"_id": savedId})


app.run()