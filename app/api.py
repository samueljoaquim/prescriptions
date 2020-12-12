import uuid

import logging

import flask
from flask import request

from bson.json_util import dumps

from services import prescriptions

from exceptions import PrescriptionsException, MalformedRequestException

from models.validators import validatePrescriptionInputData

logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = flask.Flask(__name__)
app.config['DEBUG'] = False


@app.route('/prescriptions', methods=['POST'])
def addPrescription():
    """
    [POST] - /prescriptions
    Validate clinic, physician and patient ids, save metrics and
    return the prescription request data with and added id

    For complete documentation, refer to the swagger.yml file on the project root.
    """
    rid = uuid.uuid4().hex
    try:

        #get input data and validate
        logger.debug('%s|Getting prescription data from POST', rid)
        prescriptionData = request.json
        logger.debug('%s|Prescription data: %s. Saving prescription.', rid, prescriptionData)

        logger.debug('%s|Validating prescription data',rid)
        if not validatePrescriptionInputData(rid, prescriptionData):
            raise MalformedRequestException()

        #save prescription
        entry = prescriptions.savePrescription(rid, prescriptionData)

        #convert MongoDB generated "_id" attribute to proper "id"
        entry["id"] = entry["_id"]
        entry.pop("_id", None)
        logger.debug('%s|Prescription saved: %s', rid, entry)

        #return correct output data
        return dumps({"data": entry}), 201

    except PrescriptionsException as exc:
        #Known errors, with correct codes and message
        logger.exception('%s|Application error executing the service', rid)
        return dumps({
            "error": {
                "message": exc.message,
                "code": "{:02d}".format(exc.code)
            }
        }), exc.httpstatus
    except:
        #Unknown error, return a generic error message
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
