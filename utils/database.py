import os
import pymongo

client = None

def getDb():
    global client
    if client is None:
        uri = os.getenv('PRESCRIPTIONS_MONGODB_URI', 'mongodb://localhost:27017')
        operationTimeout = os.getenv('PRESCRIPTIONS_MONGODB_OP_TIMEOUT', '15000')
        connectionTimeout = os.getenv('PRESCRIPTIONS_MONGODB_CON_TIMEOUT', '10000')

        client = pymongo.MongoClient(uri,connectTimeoutMS=connectionTimeout, socketTimeoutMS=operationTimeout)
    return client
