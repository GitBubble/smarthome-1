import soco, requests, re, sys

class Speaker:
    data = {}
    ip = None

    def getAll(self):
        speakers = soco.discover()
        self.data = {}
        speaker_data = []

        for speaker in speakers:
            speaker_info = speaker.get_speaker_info()

            speaker_data.append({
                'name' : speaker.player_name,
                'ip_address' : speaker.ip_address,
                'mac_address' : speaker_info['mac_address'],
                'software_version' : speaker_info['software_version'],
                'hardware_version' : speaker_info['hardware_version'],
                'display_version' : speaker_info['display_version'],
                'icon' : speaker_info['player_icon'],
                'uniqueid' : speaker.uid,
                'mute' : speaker.mute,
                'volume' : speaker.volume,
                'status_light' : speaker.status_light,
                'serial_number' : speaker_info['serial_number'],
                'model_name' : speaker_info['model_name'],
            })

        return speaker_data

    def mute(self):
        speaker_data = {}

        if (self.ip != None):
            speakers = soco.discover()
            speaker_exists = False

            for speaker in speakers:
                if(self.ip == speaker.ip_address):
                    speaker_exists = True

            if(speaker_exists == True):
                speaker = soco.SoCo(self.ip)

                if(speaker.mute == True):
                    mute = False
                else:
                    mute = True

                speaker.mute = mute
                speaker_data = {
                    'status' : 200,
                    'mute' : mute,
                    'uniqueid' : speaker.uid
                }
            else:
                speaker_data = {
                    'status' : 503,
                    'msg' : 'Sonos speaker are unavailable.'
                }

        else:
            speaker_data = {
                'status' : 404,
                'msg' : 'You need to defined the ip to the speaker you will connect to.'
            }

        return speaker_data

    def power(self):
        speaker_data = {}

        if (self.ip != None):
            speakers = soco.discover()
            speaker_exists = False

            for speaker in speakers:
                if(self.ip == speaker.ip_address):
                    speaker_exists = True

            if(speaker_exists == True):
                speaker = soco.SoCo(self.ip)

            else:
                speaker_data = {
                    'status' : 503,
                    'msg' : 'Sonos speaker are unavailable.'
                }

        else:
            speaker_data = {
                'status' : 404,
                'msg' : 'You need to defined the ip to the speaker you will connect to.'
            }

        return speaker_data
