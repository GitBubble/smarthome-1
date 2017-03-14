from pymongo import MongoClient
from blessings import Terminal
import time

t = Terminal()

class Hue:
    __json_data = None
    __config = None

    def __init__(self, json_data, config):
        self.__json_data = json_data
        self.__config = config

    def sensors(self):
        client = MongoClient(self.__config['mongodb']['ip'], int(self.__config['mongodb']['port']))
        db = client.smarthome

        for key, value in self.__json_data.items():
            now_date = time.strftime("%Y-%m-%d %H:%M:%S")

            sensors = {}
            for sensor in value['sensors']:
                sensors[str(sensor['state']['type'].lower())] = {
                    'value' : sensor['state']['value'],
                    'id' : sensor['id']
                }

            cursor = db.sensors.find_one({"uniqueid":key})
            if(cursor is not None):
                resualt = db.sensors.update_one({
                    'uniqueid' : str(key),
                },{
                    '$set' : {
                        'battery' : int(value['battery']),
                        'sensors' : sensors,
                        'updated_at' : now_date
                    }
                })

                print t.blue('[UPDATE] uniqueid: '+ str(key) +' | time: '+ now_date)

            else:
                resualt = db.sensors.insert_one({
                    'uniqueid' : str(key),
                    'battery' : int(value['battery']),
                    'sensors' : sensors,
                    'updated_at' : now_date,
                    'created_at' : now_date
                })

                print t.blue('[INSERT] uniqueid: '+ str(key) +' | time: '+ now_date)

        client.close()
