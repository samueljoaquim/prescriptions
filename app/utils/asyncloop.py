import asyncio

def getOrCreateEventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def getTestFuture(result):
    getOrCreateEventloop()
    f = asyncio.Future()
    f.set_result(result)
    return f
