import time
import requests
import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient(config['mongodb']['ip'], int(config['mongodb']['port']))
db = client.smarthome

loop_count = 0

while(True):
    collection = db.sensors

    for sensor in collection.find():
        print(sensor['sensors'])

        if(loop_count == 0):
            post_data = {
                'num' : sensor['sensors']['lightlevel']['id']
            }

            response = requests.post(config['restapi']['url'], data=post_data)
            data = response.json()
            print(data)

            post_data = {
                'num' : sensor['sensors']['temperature']['id']
            }

            response = requests.post(config['restapi']['url'], data=post_data)
            data = response.json()
            print(data)

        post_data = {
            'num' : sensor['sensors']['presence']['id']
        }

        response = requests.post(config['restapi']['url'], data=post_data)
        data = response.json()
        print(data)

    loop_count += 1

    if(loop_count == 60):
        loop_count = 0

    time.sleep(1)
