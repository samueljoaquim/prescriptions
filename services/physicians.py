from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=10000, ttl=172800))
def getPhysician(id):
    return id
