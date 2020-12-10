import os
import pymongo

client = None

def getDb():
    global client
    if client is None:
        uri = os.getenv('PRESCRIPTIONS_MONGODB_URI')
        operationTimeout = int(os.getenv('PRESCRIPTIONS_MONGODB_OP_TIMEOUT'))
        connectionTimeout = int(os.getenv('PRESCRIPTIONS_MONGODB_CON_TIMEOUT'))

        client = pymongo.MongoClient(uri,connectTimeoutMS=connectionTimeout, socketTimeoutMS=operationTimeout)
    return client
