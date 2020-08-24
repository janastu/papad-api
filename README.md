# About

Papad is an audio annotation framework written using Bottle WSGI framework.

# Install

Install in a virtualenv or use with sudo to install system-wide

`$ pip install -r requirements.txt`

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
