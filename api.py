from bson.json_util import dumps

import flask
from flask import request

from services import prescriptions

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("addPrescription")

app = flask.Flask(__name__)
app.config['DEBUG'] = True


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
def addPrescription():
    try:
        logger.debug('Getting prescription data from POST')
        prescriptionData = request.json
        logger.debug('Prescription data: %s. Saving prescription.', prescriptionData)

        entry = prescriptions.savePrescription(prescriptionData)
        logger.debug('Prescription saved: %s', entry)

        return dumps({"data": entry})

    except:
        logger.exception('Error executing the service')
        return dumps({
            "error": {
                "message": "generic error",
                "code": "99"
            }
        })

app.run()