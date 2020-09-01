#!/usr/bin/env python

import pymongo
import json

with open("config.json") as f:
    config = json.load(f)

client = pymongo.MongoClient("mongodb://{}:27017/".format(config['db']['host']))

db = client.papad

try:
    db.station.create_index([('station_name', pymongo.ASCENDING) ], unique=True)
except pymongo.errors.DuplicateKeyError as e:
    print("Error creating unique index on station_name")
    pass

for field in ['audio_url', 'tags', 'img_tags', 'upload_date', 'station_id']:
    try:
        db.recording.create_index([(field, pymongo.ASCENDING)])
    except Error:
        print("Error creating index on {}".format(field))
        pass

for field in ['type', 'target.source', 'target.selector.type', 'target.selector.value', 'target.selector.start', 'target.selector.end', 'body.purpose', 'body.type', 'body.value']:
    try:
        db.fragment.create_index([(field, pymongo.ASCENDING)])
    except Error:
        print("Error creating index on {}".format(field))
        pass
