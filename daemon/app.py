import sys, time, threading, requests, configparser, json
from pymongo import MongoClient
import libs.philips

config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient(config['mongodb']['ip'], int(config['mongodb']['port']))
db = client.smarthome

loop_count = 0
sensor_log = {}

""" Handler to update all devices in smart home system in the background """
class Threading(object):
    def __init__(self, interval=1):
        self.interval = interval

        print '***'

        print 'Prepare sensors in background task!'
        thread = threading.Thread(target=self.sensors, args=())
        thread.daemon = True
        thread.start()
        print 'Sensors start background'

        print '***'

        print 'Prepare lights in background task!'
        thread = threading.Thread(target=self.lights, args=())
        thread.daemon = True
        thread.start()
        print 'Sensors lights background'

        print '***'

        # print 'Prepare home audios in background task!'
        # thread = threading.Thread(target=self.home_audios, args=())
        # thread.daemon = True
        # thread.start()
        # print 'Sensors home audios background'

        print '***'

    def sensors(self):
        while True:
            r = requests.get(config['restapi']['philips_hue'] +'philips-hue/sensor-scan')
            philips_hue = libs.philips.Hue(r.json(), config)
            philips_hue.sensors()

            time.sleep(self.interval)

    def lights(self):
        while True:
            r = requests.get(config['restapi']['philips_hue'] +'philips-hue/light-scan')
            time.sleep(self.interval)

    def home_audios(self):
        while True:
            r = requests.get(config['restapi']['sonos'] +'home-audio/scan')
            time.sleep(self.interval)

threads = Threading()


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
                'uniqueid' : sensor['uniqueid'],
                'num' : sensor['sensors']['lightlevel']['id'],
                'componet' : 'sensor',
                'state' : {
                    'type' : 'lightlevel',
                    'value' : int(sensor['sensors']['lightlevel']['value'])
                }
            }

            requests.put(config['restapi']['logging'] +'logging', data=json.dumps(post_data))

        if(str(sensor_log[sensor['uniqueid']]['temperature']['value']) != str(sensor['sensors']['temperature']['value'])):
            have_changes = 1
            post_data = {
                'uniqueid' : sensor['uniqueid'],
                'num' : sensor['sensors']['temperature']['id'],
                'componet' : 'sensor',
                'state' : {
                    'type' : 'temperature',
                    'value' : int(sensor['sensors']['temperature']['value'])
                }
            }

            requests.put(config['restapi']['logging'] +'logging', data=json.dumps(post_data))

        if(str(sensor_log[sensor['uniqueid']]['presence']['value']) != str(sensor['sensors']['presence']['value'])):
            have_changes = 1
            post_data = {
                'uniqueid' : sensor['uniqueid'],
                'num' : sensor['sensors']['presence']['id'],
                'componet' : 'sensor',
                'state' : {
                    'type' : 'presence',
                    'value' : bool(sensor['sensors']['presence']['value'])
                }
            }

            requests.put(config['restapi']['logging'] +'logging', data=json.dumps(post_data))


        if(have_changes == 1):
            sensor_log[str(sensor["uniqueid"])]["lightlevel"] = sensor['sensors']['lightlevel']
            sensor_log[str(sensor["uniqueid"])]["temperature"] = sensor['sensors']['temperature']
            sensor_log[str(sensor["uniqueid"])]["presence"] = sensor['sensors']['presence']

        print('---')

    print('--- scan all sensors and update for next run --')

    loop_count += 1

    if(loop_count == 60):
        loop_count = 0

    time.sleep(1)
