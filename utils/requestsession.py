import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def getSession(retries):
    session = requests.Session()
    retryConfig = Retry(
        total=retries,
        status_forcelist=[408, 429, 500, 502, 503, 504],    #Force retries in these statuses
        method_whitelist=False                              #Allow in any HTTP method, including POST
    )
    httpadapter = HTTPAdapter(max_retries=retryConfig)
    session.mount('http://', httpadapter)
    session.mount('https://', httpadapter)
    return session


