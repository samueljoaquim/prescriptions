from bson.json_util import dumps

import flask
from flask import request

import uuid

import logging

from services import prescriptions

from exceptions import PrescriptionsException

logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = flask.Flask(__name__)
app.config['DEBUG'] = False


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
    rid = uuid.uuid4().hex
    try:
        logger.debug('%s|Getting prescription data from POST', rid)
        prescriptionData = request.json
        logger.debug('%s|Prescription data: %s. Saving prescription.', rid, prescriptionData)

        entry = prescriptions.savePrescription(rid, prescriptionData)
        logger.debug('%s|Prescription saved: %s', rid, entry)

        return dumps({"data": entry}), 201

    except PrescriptionsException as exc:
        logger.exception('%s|Application error executing the service', rid)
        return dumps({
            "error": {
                "message": exc.message,
                "code": "{:02d}".format(exc.code)
            }
        }), exc.httpstatus
    except:
        logger.exception('%s|Unknown error executing the service', rid)
        return dumps({
            "error": {
                "message": "application error",
                "code": "{:02d}".format(99)
            }
        }), 500


# Start server if main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)