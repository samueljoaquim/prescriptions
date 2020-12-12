import logging

import jsonschema

from models.schemas import prescriptionsInputSchema, prescriptionsOutputSchema, prescriptionsErrorMsgSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def validatePrescriptionInputData(rid, prescription):
    try:
        jsonschema.validate(instance=prescription, schema=prescriptionsInputSchema)
        return True
    except:
        logger.exception("%s|Error in prescription schema validation", rid)
        return False


def validatePrescriptionOutputData(rid, prescription):
    try:
        jsonschema.validate(instance=prescription, schema=prescriptionsOutputSchema)
        return True
    except:
        logger.exception("%s|Error in prescription schema validation", rid)
        return False


def validatePrescriptionErrorMsgData(rid, prescription):
    try:
        jsonschema.validate(instance=prescription, schema=prescriptionsErrorMsgSchema)
        return True
    except:
        logger.exception("%s|Error in prescription schema validation", rid)
        return False
