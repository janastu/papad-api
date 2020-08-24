import json
import bottle
from bottle import Bottle, run, request, response, abort, hook, HTTPResponse
from bottle.ext.mongo import MongoPlugin
from truckpad.bottle.cors import CorsPlugin, enable_cors

from bson.json_util import dumps
from bson.objectid import ObjectId

app = Bottle()

with open("config.json") as f:
    app.config.load_dict(json.load(f))

plugin = MongoPlugin(uri="mongodb://{}".format(app.config['db.host']), db=app.config['db.name'], json_mongo=True)
app.install(plugin)

ENTITY_COLLECTION_MAP = {
        'channels': 'station',
        'recordings': 'recording'
        }

def raise_error(message, code=400):
    raise HTTPResponse(
            body=json.dumps({ "message": message }),
            status=code,
            headers={ 'Content-type': 'application/json' }
            )

def check_path(entity):
    if not entity in ENTITY_COLLECTION_MAP:
        raise_error('{} not found'.format(entity), code=404)

@enable_cors
@app.route('/<entity>/')
def channels(mongodb, entity):
    check_path(entity)
    response.content_type = 'application/json'
    return dumps(mongodb[ENTITY_COLLECTION_MAP[entity]].find())

@enable_cors
@app.route('/<entity>/<id>')
def channel(mongodb, entity, id):
    check_path(entity)
    if len(id) == 24:
        obj = mongodb[ENTITY_COLLECTION_MAP[entity]].find_one({'_id': ObjectId(id)})
    else:
        obj = mongodb[ENTITY_COLLECTION_MAP[entity]].find_one({'_id': id})

    if obj:
        return obj
    else:
        raise_error('{} not found'.format(ENTITY_COLLECTION_MAP[entity]), code=404)

@enable_cors
@app.route('/<entity>/', method='POST')
def post_channel(mongodb, entity):
    check_path(entity)
    obj = request.json
    if not obj:
        raise_error('No data received')

    if entity == 'recordings':
        station = mongodb['station'].find_one({'station_name': obj['station_name']})
        if not station:
            raise_error('Station does not exist')
        obj['station_id'] = station['_id'] 
    #entity = json.loads(data)
    try:
        mongodb[ENTITY_COLLECTION_MAP[entity]].save(obj)
    except Exception as e:
        raise_error(str(e))

@enable_cors
@app.route('/<entity>/<id>', method='PUT')
def put_channel(mongodb, entity, id):
    check_path(entity)
    if len(id) == 24:
        obj = mongodb[ENTITY_COLLECTION_MAP[entity]].find_one({'_id': ObjectId(id)})
    else:
        obj = mongodb[ENTITY_COLLECTION_MAP[entity]].find_one({'_id': id})

    if not request.json:
        raise_error('No data received')

    if obj:
        updated_obj = request.json
        if entity == 'recordings':
            station = None
            if 'station_name' in updated_obj:
                station = mongodb['station'].find_one({ 'station_name': updated_obj['station_name'] })
            elif 'station_id' in updated_obj:
                if len(updated_obj['station_id']) == 24:
                    station = mongodb['station'].find_one({'_id': ObjectId(updated_obj['station_id'])})
                else:
                    station = mongodb['station'].find_one({'_id': updated_obj['station_id']})
            if station:
                obj['station_id'] = station['_id']
        obj.update(updated_obj)
        mongodb[ENTITY_COLLECTION_MAP[entity]].update_one(
                { '_id': obj['_id'] },
                { "$set": obj }
                )
        return obj
    else:
        raise_error('{} not found'.format(ENTITY_COLLECTION_MAP[entity]), code=404)

app.install(CorsPlugin(origins=['*']))

if __name__ == '__main__':
    run(app, host=app.config['server.host'], port=app.config['server.port'], reloader=True)
else:
    application = app
