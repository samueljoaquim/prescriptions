# prescriptions
iClinic Python Challenge implementation


## Introduction
This is an implementation of the [iClinic Python Challenge](https://github.com/iclinic/iclinic-python-challenge). It is a REST API as described in this link, taking on consideration all the required services, and using *MongoDB* as the backing database. Let's get started!


## Project Structure
The root of the project is structured as follows:
```
prescriptions
├── app
│   ├── api.py
│   ├── exceptions.py
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── models
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── clinics.py
│   │   ├── metrics.py
│   │   ├── patients.py
│   │   ├── physicians.py
│   │   └── prescriptions.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   ├── test_clinics.py
│   │   ├── test_metrics.py
│   │   ├── test_patients.py
│   │   ├── test_physicians.py
│   │   ├── test_prescriptions.py
│   │   └── test_utils.py
│   └── utils
│       ├── __init__.py
│       ├── database.py
│       └── requestsession.py
├── docker-compose.dev.env
├── docker-compose.yml
├── Dockerfile
├── Pipfile
├── README.md
└── sourceenv.sh
```

The *app* directory contains the application itself. The *api.py* file is the main application, that executes the Flask server and acts as the controller. *services* contains all internal services (*prescriptions.py*) and external APIs calls (all other modules). *models* contains the schemas to validate inputs and outputs for the services. *tests* contains the unit tests. *utils* contains useful functions that are shared by several modules.

This application uses *pipenv* as the virtual environment and dependencies management tool. Once it is installed, you can run ```pipenv install``` inside the *app* directory and it will install all dependencies. To run the application directly, without using docker, run ```pipenv run python3 api.py``` from inside the *app* directory. **Don't forget to set all the necessary environment variables as shown below.**


### Environment Variables
You must set the following environment variables before running the application:

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


## Creating the Docker Images
Before running the service, it is necessary to create a Docker image, which is very straightforward. Please make sure that you have *docker* and *docker-compose* commands installed on you machine before. Then, go to the root of the project in a shell and run:
```
docker build . -t prescriptions
```
Now, the docker image should be locally available as ```prescriptions:latest```.


## Running the Service
Once you have the docker image built, you can start a local docker container by running:
```
docker-compose up
```
This will bring up not only a *prescriptions* service container (aliased *prescriptionssvc*), but also a *mongodb* container (aliased *prescriptionsdb* in the docker network). All the environment variables are located inside the *docker-compose.dev.env* file, and the database URI (**PRESCRIPTIONS_MONGODB_URI**) is already pointing to this *mongodb* instance. **Make sure that you have no applications running on ports 5000 (prescriptions service) and 27017 (mongodb) before, since those are the default ports.**

If you need to point to another mongodb instance, modify the *docker-compose.dev.env* file with the correct URI. Also, you can remove or comment out the following service from the *docker-compose.yml* file:
```
  prescriptionsdb:
    image: mongo:latest
    ports:
      - "27017:27017"
    networks:
      prescriptions_net:
        aliases:
        - prescriptionsdb
```


## Making Requests
Once your service is up and running, you can start making requests to it. You can use a tool like *RESTED* for making sure it's working (available for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/rested/) and [Chrome](https://chrome.google.com/webstore/detail/rested/eelcnbccaccipfolokglfhhmapdchbfg)).

The endpoint will be ```http://127.0.0.1:5000```, and the path ```/prescriptions```. Choose ```POST``` as the method and send a ```Content-Type: application/json``` header. Also, use a ```Custom``` request body with the following contents:
```
{
  "clinic": {
    "id": 1
  },
  "physician": {
    "id": 1
  },
  "patient": {
    "id": 1
  },
  "text": "Dipirona 1x ao dia"
}
```
If you get any response, then the server is running. If all the external services are working as well, you will most likely get a *201* response status. Otherwise, the service will show an error message identifying what's wrong.


## Querying the Database
If you are running the MongoDB instance as configured in the *docker-compose.yml*, it is possible to check if the data is being saved correctly in the database. First, enter a MongoDB shell inside the mogno container through the following shorthand command:
```
docker exec -it `docker ps|sed -n 's/.*\(prescriptions_prescriptionsdb.*\)/\1/gp'` mongo
```
Then, once in the mongodb shell, run the following commands:
```
use prescriptions
db.prescriptions.findOne()
```
If the data is being saved correctly, you should see an output like this:
```
{
        "_id" : ObjectId("5fd265500b7378780c7508b6"),
        "clinic" : {
                "id" : 1
        },
        "physician" : {
                "id" : 1
        },
        "patient" : {
                "id" : 1
        },
        "text" : "Dipirona 1x ao dia"
}

```


## Running Unit Tests With Coverage
This project uses *nose* for unit testing, along with the *coverage* plugin for it. To execute the tests and get the coverage report, simply run:
```
pipenv run nosetests --with-coverage --cover-package=api,services,utils,exceptions
```
You can also run the tests inside a running docker container:
```
docker exec -it `docker ps|sed -n 's/.*\(prescriptions_prescriptionssvc.*\)/\1/gp'` pipenv run nosetests --with-coverage --cover-package=api,services,utils,exceptions
```
