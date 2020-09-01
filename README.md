# About

Papad is an audio annotation framework written using Bottle WSGI framework.

# Install

Install in a virtualenv or use with sudo to install system-wide

`$ pip install -r requirements.txt`

For enabling avahi service, copy the file `avahi/papad.service` to /etc/avahi/services. You can run the command

`$ sudo cp avahi/papad.service /etc/avahi/services/`

To copy and enable service discovery through zero-conf.

# Configure

Copy config.json.example to config.json and edit the values. Put in appropriate values for the mongodb host and name of the database as well as the server host and port to run on.

# Run

`$ python main.py`

# Docker

To run using docker

```

$ cd docker/
$ docker-compose build
$ docker-compose up -d

```

# Query

The list endpoints /channels/, /recordings/ and others support query parameters of the type field_name=field_value. 
The also support mongo query values such as /channels/?station_name={"$regex": ".*somestring.*"} , to search for 
'somestring' within the field `station_name`
