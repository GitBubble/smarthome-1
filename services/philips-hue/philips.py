import requests
import re

class Hue:
    data = {}

    __bridge_url = ''
    __light_num = 0
    __hue_bri_max = 254

    def __init__(self, bridge, username):
        self.__bridge_url = 'http://'+ bridge +'/api/'+ username +'/'

    def getLightData(self,num=0):
        self.data = {}
        self.__light_num = int(num)

        if(self.__light_num > 0):
            response = requests.get(self.__bridge_url +'lights/'+ str(self.__light_num))
        else:
            response = requests.get(self.__bridge_url +'lights')

        self.data = response.json()

    def __handleLight(self,state, light_num):
        if(state == True):
            if((str(light_num) in self.data and self.data[light_num]['state']['on'] == True) or ('state' in self.data and self.data['state']['on'] == True) ):
                print('Light: '+ str(light_num) +' is on')
            else:
                r = requests.put(self.__bridge_url +'lights/'+ str(light_num) +'/state', json={"on": True, "bri": int(self.__hue_bri_max)})
                print(r.status_code)
        elif(state == False):
            if((str(light_num) in self.data and self.data[light_num]['state']['on'] == False) or ('state' in self.data and self.data['state']['on'] == False) ):
                print('Light: '+ str(light_num) +' is off')
            else:
                r = requests.put(self.__bridge_url +'lights/'+ str(light_num) +'/state', json={"on": False})
                print(r.status_code)

    def lightOn(self,state):
        if(self.__light_num > 0):
            self.__handleLight(state, self.__light_num)
        else:
            for lights in self.data:
                self.__handleLight(state, lights)

    def findAllSensors(self):
        self.data = {}
        response = requests.get(self.__bridge_url +'sensors')
        self.data = response.json()

        sensors = {}

        for data in self.data:
            if('uniqueid' in self.data[data]):
                uniqueid = str(self.data[data]['uniqueid'].split('-')[0])
            else:
                continue

            if(len(uniqueid.split(':')) != 8):
                continue

            if(uniqueid not in sensors):
                sensors[uniqueid] = {
                    'uniqueid' : uniqueid,
                    'battery' : None,
                    'modelid' : str(self.data[data]['modelid']),
                    'sensors' : []
                }

            tmp_sensor = {
                'id' : str(data),
                'state' : {}
            }


            if(self.data[data]['type'] == 'ZLLPresence'):
                tmp_sensor['state'] = {
                    'type' : 'Presence',
                    'presence' : str(self.data[data]['state']['presence'])
                }

            if(self.data[data]['type'] == 'ZLLTemperature'):
                tmp_sensor['state'] = {
                    'type' : 'Temperature',
                    'temperature' : int(self.data[data]['state']['temperature'])
                }

            if(self.data[data]['type'] == 'ZLLLightLevel'):
                tmp_sensor['state'] = {
                    'type' : 'LightLevel',
                    'lightlevel' : int(self.data[data]['state']['lightlevel'])
                }

            if(sensors[uniqueid]['battery'] is None and 'config' in self.data[data] and 'battery' in self.data[data]['config'] and self.data[data]['config']['battery'] != 'None'):
                sensors[uniqueid]['battery'] = int(self.data[data]['config']['battery'])

            sensors[uniqueid]['sensors'].append(tmp_sensor)

        return sensors

    def getSensorData(self, num):
        response = requests.get(self.__bridge_url +'sensors/'+ num)
        self.data = {}
        self.data = response.json()

        uniqueid = str(self.data['uniqueid'].split('-')[0])

        sensor = {
            'uniqueid' : uniqueid,
            'modelid' : self.data['modelid'],
            'swversion' : self.data['swversion'],
            'type' : None,
            'state' : {}
        }

        if(self.data['type'] == 'ZLLPresence'):
            sensor['type'] = 'presence'
            sensor['state'] = {
                'value' : 1 if self.data['state']['presence'] == True else 0
            }

        elif(self.data['type'] == 'ZLLTemperature'):
            sensor['type'] = 'temperature'
            sensor['state'] = {
                'value' : int(self.data['state']['temperature'])
            }

        elif(self.data['type'] == 'ZLLLightLevel'):
            sensor['type'] = 'lightlevel'
            sensor['state'] = {
                'value' : int(self.data['state']['lightlevel'])
            }

        return sensor
