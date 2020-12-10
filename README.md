# prescriptions
iClinic Python Challenge implementation

## Creating the Docker Images

## Running the Service

### Environment Variables
For running this service, you must set the following environment variables on Docker before proceeding:

- **PRESCRIPTIONS_MONGODB_URI** - access URI for the MongoDB that contains the service database
- **PRESCRIPTIONS_ENDPOINT** - endpoint for services. For this service, it was assumed that all provided services (except the database)
are under the same endpoint under different paths

- **PRESCRIPTIONS_CLINIC_PATH** - path to the *clinics* service on the endpoint
- **PRESCRIPTIONS_CLINIC_TOKEN** - *clinics* service Bearer token
- **PRESCRIPTIONS_CLINIC_TIMEOUT** - *clinics* service request timeout
- **PRESCRIPTIONS_CLINIC_RETRIES** - *clinics* service retries on timeout or the HTTP status refered below

- **PRESCRIPTIONS_METRICS_PATH** - path to the *metrics* service on the endpoint
- **PRESCRIPTIONS_METRICS_TOKEN** - *metrics* service Bearer token
- **PRESCRIPTIONS_METRICS_TIMEOUT** - *metrics* service request timeout
- **PRESCRIPTIONS_METRICS_RETRIES** - *metrics* service retries on timeout or the HTTP status refered below

- **PRESCRIPTIONS_PATIENTS_PATH** - path to the *patients* service on the endpoint
- **PRESCRIPTIONS_PATIENTS_TOKEN** - *patients* service Bearer token
- **PRESCRIPTIONS_PATIENTS_TIMEOUT** - *patients* service request timeout
- **PRESCRIPTIONS_PATIENTS_RETRIES** - *patients* service retries on timeout or the HTTP status refered below

- **PRESCRIPTIONS_PHYSICIAN_PATH** - path to the *physician* service on the endpoint
- **PRESCRIPTIONS_PHYSICIAN_TOKEN** - *physician* service Bearer token
- **PRESCRIPTIONS_PHYSICIAN_TIMEOUT** - *physician* service request timeout
- **PRESCRIPTIONS_PHYSICIAN_RETRIES** - *physician* service retries on timeout or the HTTP status refered below

Apart from an unresponsive server, the HTTP statuses returned that will cause a new retry on all services are these:
- 408 (*Request Timeout*)
- 429 (*Too Many Requests*)
- 500 (*Internal Server Error*)
- 502 (*Bad Gateway*)
- 503 (*Service Unavailable*)
- 504 (*Gateway Timeout*)

## Running Unit Tests With Coverage
This project uses *nose* for unit testing, along with the *coverage* plugin for it. To execute the tests and get the coverage report, simply run:
```
nosetests --with-coverage --cover-package=api,services,utils,exceptions
```
If you want to add other packages to the coverage, just add the package names comma-separated to the ```cover-pagkace``` parameter.
If you're running through *pipenv*, prefix the command above with ```pipenv run ```. If you're using another virtual environment tool, check the specific documentation for it.
