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
            speaker_data.append({
                'name' : speaker.player_name,
                'ip' : speaker.ip_address,
                'uniqueid' : speaker.uid
            })

        return speaker_data
