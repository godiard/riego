# jobs management
import json
import schedule
import time

from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import gpiozero
except Exception:
    import fakegpio as gpiozero

CONFIG_FILE_NAME = 'config.json'


class IrrigationManager:

    def __init__(self):
        self.config = self.read_config()
        self.relays = None
        self.init_relays()
        self.init_scheduled_tasks(self.config)

    def read_config(self):
        config = None
        with open(CONFIG_FILE_NAME) as config_file:
            try:
                config = json.load(config_file)
            except Exception:
                print('Error reading json config file')
        return config

    def start_irrigation(self, port, power_port):
        # open zone port
        print(datetime.now())
        self.relays[port].on()
        # open power port
        self.relays[power_port].on()

    def stop_irrigation(self, port, power_port):
        print(datetime.now())
        # close power port
        self.relays[power_port].off()
        # close zone port
        self.relays[port].off()

    def init_relays(self):
        self.relays = {}
        power_port = self.config['power']['port']
        print('Initilize power rele, port %d' % power_port)
        power_relay = gpiozero.OutputDevice(
            power_port, active_high=False, initial_value=False)
        self.relays[power_port] = power_relay

        for zone in self.config['zones']:
            print('Initialize zone %s, port %d' % (zone['name'], zone['port']))
            zone_relay = gpiozero.OutputDevice(
                zone['port'], active_high=False, initial_value=False)
            self.relays[zone['port']] = zone_relay

    def init_scheduled_tasks(self, config):
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
                    self.start_irrigation, zone['port'], power_port)
                print('schedule end of zone %s: %s' %
                      (zone['name'], zone['end']))
                schedule.every().day.at(zone['end']).do(
                    self.stop_irrigation, zone['port'], power_port)

    def update_config(self, event):
        print('CONFIG FILE UPDATED')
        updated_config = self.read_config()
        if updated_config is not None:
            if updated_config != self.config:
                self.config = updated_config
                if self.config:
                    self.init_scheduled_tasks(self.config)


irrigation_manager = IrrigationManager()

event_handler = FileSystemEventHandler()
event_handler.on_modified = irrigation_manager.update_config

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
