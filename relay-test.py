# based on https://raspberrypi.stackexchange.com/a/120470/130766
import sys
import time

import gpiozero

if len(sys.argv) < 3:
    print('Use %s port time' % sys.argv[0])
    exit()

RELAY_PIN = sys.argv[1]
SECONDS = int(sys.argv[2])

# Triggered by the output pin going high: active_high=True
# Initially off: initial_value=False

relay = gpiozero.OutputDevice(
    RELAY_PIN, active_high=False, initial_value=False)

relay.on() # switch off
time.sleep(SECONDS)
relay.off() # switch on

print(relay.value) # see if on or off

