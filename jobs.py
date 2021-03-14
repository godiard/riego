# jobs management
import json
import schedule
import time

from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_FILE_NAME = 'config.json'

config = None


def read_config():
    config = None
    with open(CONFIG_FILE_NAME) as config_file:
        try:
            config = json.load(config_file)
        except Exception:
            print('Error reading json config file')
    return config


def start_irrigation(port, power_port):
    # open zone port
    print(datetime.now())
    print('Open zone port %s' % port)
    # open power port
    print('Open power port %s' % power_port)


def stop_irrigation(port, power_port):
    print(datetime.now())
    # close zone port
    print('Close zone port %s' % port)
    # close power port
    print('Close power port %s' % power_port)


def init_scheduled_tasks(config):
    print('config: %s' % config)
    power_port = config['power']['port']
    schedule.clear()
    for zone in config['zones']:
        # zone['start'] have the format '22:30'
        # from https://stackoverflow.com/a/30393162/3969110
        if zone['enabled']:
            print('schedule start of zone %s: %s' %
                  (zone['name'], zone['start']))
            schedule.every().day.at(zone['start']).do(
                start_irrigation, zone['port'], power_port)
            print('schedule end of zone %s: %s' %
                  (zone['name'], zone['end']))
            schedule.every().day.at(zone['end']).do(
                stop_irrigation, zone['port'], power_port)


def update_config(event):
    global config
    print('CONFIG FILE UPDATED')
    updated_config = read_config()
    if update_config is not None:
        if updated_config != config:
            config = updated_config
            if config:
                init_scheduled_tasks(config)


config = read_config()
init_scheduled_tasks(config)

event_handler = FileSystemEventHandler()
event_handler.on_modified = update_config

observer = Observer()
observer.schedule(event_handler, CONFIG_FILE_NAME, recursive=False)
observer.start()
try:
    while True:
        schedule.run_pending()
        time.sleep(30)  # wait 30 seconds
except KeyboardInterrupt:
    observer.stop()
observer.join()
