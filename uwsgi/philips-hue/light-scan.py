import os, sys, requests, re, json, configparser, falcon, libs.philips

dir_path = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(dir_path +'/config.ini')

class ObjResource:
    def on_get(self, req, resp):
        PhilipsHue = libs.philips.Hue(config['philips.hue']['ip'],config['philips.hue']['username'])
        lights = PhilipsHue.findAllLights()
        resp.body = json.dumps(lights)

api = falcon.API()
api.add_route('/philips-hue/light-scan', ObjResource())
