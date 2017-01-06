import soco
import requests
import re
import sys

class Speaker:
    data = {}

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
                'uniqueid' : speaker.uid,
                'mute' : speaker.mute,
                'volume' : speaker.volume,
                'status_light' : speaker.status_light,
                'serial_number' : speaker_info['serial_number'],
                'model_name' : speaker_info['model_name'],
            })

        return speaker_data
