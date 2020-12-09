import os
import pymongo

client = None

def getDb():
    global client
    if client is None:
        url = os.getenv('PRESCRIPTIONS_MONGODB_URL', 'mongodb://localhost:27017')
        client = pymongo.MongoClient(url)
    return client.prescriptions
