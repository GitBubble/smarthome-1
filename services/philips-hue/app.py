import json
import sys
import configparser
import philips

config = configparser.ConfigParser()
config.read('../services/philips-hue/config.ini')

argv = {}

for sys_argv in sys.argv:
    split_argv = sys_argv.split('=')
    if(len(split_argv) > 1):
        argv[split_argv[0]] = split_argv[1]

PhilipsHue = philips.Hue(config['philips.hue']['ip'],config['philips.hue']['username'])

if(argv['mode'] == 'light'):
    if('do' in argv and argv['do'] == 'scan'):
        lights = PhilipsHue.findAllLights()
        print(json.dumps(lights))

    else:
        light_number = 0

        if('num' in argv):
            light_number =  int(argv['num'])

        PhilipsHue.getLightData(light_number)

        if PhilipsHue.data:
            if(argv['light'] == 'on'):
                PhilipsHue.lightOn(True)
                print(json.dumps(PhilipsHue.light_status))
            elif(argv['light'] == 'off'):
                PhilipsHue.lightOn(False)
                print(json.dumps(PhilipsHue.light_status))
            else:
                print('State are wrong')

        else:
            print('light not found')

elif(argv['mode'] == 'sensor'):
    if(argv['do'] == 'scan'):
        sensors = PhilipsHue.findAllSensors()
        print(json.dumps(sensors))

    elif (argv['do'] == 'get'):
        sensors = PhilipsHue.getSensorData(argv['num'])
        print(json.dumps(sensors))

    else:
        print('wrong do command')

else:
    print('you need to pick a Philips Hue mode')
