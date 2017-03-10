import os, sys, requests, re, json, configparser, falcon, libs.philips
from blessings import Terminal

dir_path = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(dir_path +'/config.ini')

t = Terminal()

class ObjResourceLightScan:
    def on_get(self, req, resp):
        PhilipsHue = libs.philips.Hue(config['philips.hue']['ip'],config['philips.hue']['username'])
        lights = PhilipsHue.findAllLights()
        resp.body = json.dumps(lights)

class ObjResourceLight:
    def on_post(self, req, resp):
        print t.blue('Do a request!')

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

            print t.red('Invalidate json input data from client')

        if(json_input_found == True):
            PhilipsHue = libs.philips.Hue(config['philips.hue']['ip'],config['philips.hue']['username'])

            light_number = 0
            if 'num' in json_data.keys():
                light_number =  int(json_data['num'])

            PhilipsHue.getLightData(light_number)

            if PhilipsHue.data:
                if 'on' in json_data.keys():
                    if(json_data['on'] == 1):
                        PhilipsHue.lightOn(True)
                        print t.blue('Light stauts:\n'+ json.dumps(PhilipsHue.light_status))

                    elif(json_data['on'] == 0):
                        PhilipsHue.lightOn(False)
                        print t.blue('Light stauts:\n'+ json.dumps(PhilipsHue.light_status))

                    else:
                        print t.red('Wrong value for params[on] : '+ str(json_data['on']))

                    resp.body = json.dumps(PhilipsHue.light_status)
            else:
                if(PhilipsHue.bridge_online == False):
                    resp.body = {
                        'status' : '404',
                        'msg' : 'Philips Hue Bridge is offline'
                    }
                    print t.yellow('Philips Hue Bridge is offline')

                else:
                    resp.body = {
                        'status' : '404',
                        'msg' : 'Philip Hue found no lights'
                    }
                    print t.yellow('Philip Hue found no lights')

api = falcon.API()
api.add_route('/philips-hue/light-scan', ObjResourceLightScan())
api.add_route('/philips-hue/light', ObjResourceLight())
