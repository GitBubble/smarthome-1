import time
import requests
import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient(config['mongodb']['ip'], int(config['mongodb']['port']))
db = client.smarthome

loop_count = 0
sensor_log = {}

while(True):
    collection = db.sensors

    for sensor in collection.find():
        have_changes = 0

        if(sensor['uniqueid'] not in sensor_log.keys()):
            sensor_log[str(sensor['uniqueid'])] = {
                'lightlevel' : {
                    'id' : '',
                    'value' : ''
                },
                'temperature' : {
                    'id' : '',
                    'value' : ''
                },
                'presence' : {
                    'id' : '',
                    'value' : ''
                }
            }

            print('not exists')


        print(sensor['uniqueid'])
        print('LightLevel: '+ str(sensor_log[sensor['uniqueid']]['lightlevel']['value']) +' => '+ str(sensor['sensors']['lightlevel']['value']))
        print('Temperature: '+ str(sensor_log[sensor['uniqueid']]['temperature']['value']) +' => '+ str(sensor['sensors']['temperature']['value']))
        print('Presence: '+ str(sensor_log[sensor['uniqueid']]['presence']['value']) +' => '+ str(sensor['sensors']['presence']['value']))

        if(str(sensor_log[sensor['uniqueid']]['lightlevel']['value']) != str(sensor['sensors']['lightlevel']['value'])):
            have_changes = 1
            post_data = {
                'num' : sensor['sensors']['lightlevel']['id']
            }
            requests.post(config['restapi']['url'] +'sensors/log', data=post_data)

        if(str(sensor_log[sensor['uniqueid']]['temperature']['value']) != str(sensor['sensors']['temperature']['value'])):
            have_changes = 1
            post_data = {
                'num' : sensor['sensors']['temperature']['id']
            }
            requests.post(config['restapi']['url'] +'sensors/log', data=post_data)

        if(str(sensor_log[sensor['uniqueid']]['presence']['value']) != str(sensor['sensors']['presence']['value'])):
            have_changes = 1
            post_data = {
                'num' : sensor['sensors']['presence']['id']
            }
            requests.post(config['restapi']['url'] +'sensors/log', data=post_data)


        if(have_changes == 1):
            sensor_log[str(sensor["uniqueid"])]["lightlevel"] = sensor['sensors']['lightlevel']
            sensor_log[str(sensor["uniqueid"])]["temperature"] = sensor['sensors']['temperature']
            sensor_log[str(sensor["uniqueid"])]["presence"] = sensor['sensors']['presence']

        print('---')
        
    print('--- scan all sensors and update for next run --')
    requests.post(config['restapi']['url'] +'sensors/scan', data=post_data)

    loop_count += 1

    if(loop_count == 60):
        loop_count = 0

    time.sleep(1)
