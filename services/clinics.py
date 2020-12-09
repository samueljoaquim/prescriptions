from cachetools import cached, TTLCache
from utils import requestsession

@cached(cache=TTLCache(maxsize=10000, ttl=259200))
def getClinic(id):
    #request = requestsession.getSession(retries, bearertoken)
    return id
