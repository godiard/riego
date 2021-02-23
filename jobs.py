# jobs management
import json
import schedule
import time

CONFIG_FILE_NAME = 'config.json'


def read_config():
    with open(CONFIG_FILE_NAME) as config_file:
        config = json.load(config_file)
    return config


def start_irrigation(port, power_port):
    # open zone port
    print('Open zone port %s' % port)
    # open power port
    print('Open power port %s' % power_port)


def stop_irrigation(port, power_port):
    # close zone port
    print('Close zone port %s' % port)
    # close power port
    print('Close power port %s' % power_port)


def init_scheduled_tasks(config):
    power_port = config['power']['port']
    for zone in config['zones']:
        # zone['start'] have the format '22:30'
        # from https://stackoverflow.com/a/30393162/3969110
        print('schedule start of zone %s: %s' % (zone['name'], zone['start']))
        schedule.every().day.at(zone['start']).do(
            start_irrigation, zone['port'], power_port)
        print('schedule end of zone %s: %s' % (zone['name'], zone['end']))
        schedule.every().day.at(zone['end']).do(
            stop_irrigation, zone['port'], power_port)


config = read_config()
print(config)
init_scheduled_tasks(config)

while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute
