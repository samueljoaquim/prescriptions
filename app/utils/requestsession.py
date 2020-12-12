from aiohttp_retry import RetryClient, RetryOptions

def getSession(retries):
    options = RetryOptions(
        attempts=retries,
        statuses=[408, 429, 500, 502, 503, 504],
    )
    return RetryClient(retry_options=options)


async def doGetJsonRequest(url,retries,timeout,bearerToken):
    request = getSession(retries)
    try:
        data = None
        request._client.headers.update({"Content-Type": "application/json"})
        request._client.headers.update({"Authorization": "Bearer "+bearerToken})
        async with request.get(url, timeout=timeout) as response:
            data = await response.json()
            return response.status, data
    finally:
        await request.close()


async def doPostJsonRequest(url,data,retries,timeout,bearerToken):
    request = getSession(retries)
    try:
        data = None
        request._client.headers.update({"Content-Type": "application/json"})
        request._client.headers.update({"Authorization": "Bearer "+bearerToken})
        async with request.post(url, timeout=timeout, data=data) as response:
            data = await response.json()
            return response.status, data
    finally:
        await request.close()
