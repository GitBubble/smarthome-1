import os, sys, requests, re, json, configparser, falcon, libs.sonos
from blessings import Terminal

dir_path = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(dir_path +'/config.ini')

t = Terminal()

class ObjResourceSensorScan:
    def on_get(self, req, resp):
        Sonos = libs.sonos.Speaker()
        sonos_data = Sonos.getAll()
        print sonos_data
        resp.body = json.dumps(sonos_data)

api = falcon.API()
api.add_route('/sonos/speaker-scan', ObjResourceSensorScan())
#
#
# Sonos = libs.sonos.Speaker()
# sonos_data = Sonos.getAll()
# print json.dumps(sonos_data)
