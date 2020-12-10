#/bin/bash

#This file sources all the docker-compose.dev entries in a bash shell...
for e in `cat docker-compose.dev.env`; do export $e; done

#...and changes the database to a localhost instance
PRESCRIPTIONS_MONGODB_URI=mongodb://localhost:27017

#Useful for running standalone app, without the need to use docker.