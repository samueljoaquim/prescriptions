from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=10000, ttl=43200))
def getPatient(id):
    return id
