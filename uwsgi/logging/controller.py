
import os, sys, requests, re, json, configparser, falcon, pymongo, time
from pymongo import MongoClient
from blessings import Terminal

dir_path = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(dir_path +'/config.ini')

t = Terminal()

class ObjResourceLogging:
    def on_get(self, req, resp):
        print 'get'

    def on_put(self, req, resp):
        json_input_found = False

        try:
            json_data = json.loads(req.stream.read())
            json_input_found = True
            print t.green('Json data from client its validated')
        except:
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({
                'status' : '404',
                'message' : 'Your json input data is not validated.'
            })

        if(json_input_found == True):
            client = MongoClient(config['mongodb']['ip'], int(config['mongodb']['port']))
            db = client.smarthome

            now_date = time.strftime("%Y-%m-%d %H:%M:%S")
            resualt = db.logging.insert_one({
                'uniqueid' : str(json_data['uniqueid']),
                'component' : str(json_data['componet']),
                'created_at' : now_date,
                'state' : json_data['state']
            })

            print t.blue('[INSERT] logging on uniqueid: '+ str(json_data['uniqueid']) +' | time: '+ now_date)

            client.close()

api = falcon.API()
api.add_route('/logging', ObjResourceLogging())
