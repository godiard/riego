# a fake library to test the code out of the raddspberry

class OutputDevice:

    def __init__(self, pin, active_high=False, initial_value=False):
        self._pin = pin
        self._active_high = active_high
        self._initial_value = initial_value

    def on(self):
        print('FAKE RELE port %d ON' % self._pin)

    def off(self):
        print('FAKE RELE port %d OFF' % self._pin)
