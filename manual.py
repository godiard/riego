import sys
import time

from irrigation import IrrigationManager

irrigation_manager = IrrigationManager()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage is: python3 manual.py zone (number) minutes')
        for n, zone in enumerate(irrigation_manager.config['zones']):
            print('[%d] = %s' % (n, zone['name']))
    else:
        zone_number = int(sys.argv[1])
        minutes = int(sys.argv[2])
        zone = irrigation_manager.config['zones'][zone_number]
        print('Start zone %s, %d minutes' % (zone['name'], minutes))

        power_port = irrigation_manager.config['power']['port']
        zone_port = zone['port']
        irrigation_manager.start_irrigation(zone_port, power_port)
        time.sleep(30 * minutes)
        irrigation_manager.stop_irrigation(zone_port, power_port)
