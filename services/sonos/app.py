import json
import sys
import configparser
import sonos

argv = {}

for sys_argv in sys.argv:
    split_argv = sys_argv.split('=')
    if(len(split_argv) > 1):
        argv[split_argv[0]] = split_argv[1]

if(argv['mode'] == 'speaker'):
    if('do' in argv and argv['do'] == 'scan'):
        Sonos = sonos.Speaker()
        sonos_data = Sonos.getAll()

        print(json.dumps(sonos_data))

    elif('do' in argv and argv['do'] == 'mute'):
        Sonos = sonos.Speaker()
        Sonos.ip = argv['ip']
        sonos_data = Sonos.mute()

        print(json.dumps(sonos_data))

    elif('do' in argv and argv['do'] == 'power'):
        Sonos = sonos.Speaker()
        Sonos.ip = argv['ip']
        sonos_data = Sonos.power()

        print(json.dumps(sonos_data))


# speaker.player_name = 'My own speaker'
# play() / pause()
