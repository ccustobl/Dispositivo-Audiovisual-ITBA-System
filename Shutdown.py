# --------------------------------------------------

"""App that controls the shutdown protocol"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import subprocess
import time
import RPi.GPIO as GPIO
import APP_Config

from Drivers.DRV_Switch import Switch

# --------------------------------------------------

class Shutdown:
    """RPi Shutdown Protocol Control"""

# --------------------------------------------------

    def __init__(self):
        """Initialization"""

        # Pin Initizalization
        self._pin = APP_Config.PIN_SHUTDOWN
        self.switch_shutdown = Switch(APP_Config.PIN_SHUTDOWN, True, self.cb_turn_off)
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(self._pin, GPIO.RISING, callback=self.cb_turn_off, bouncetime=200)

# --------------------------------------------------

    def cb_turn_off(self, *args):
        """Callback that turns off the RPi"""

        GPIO.remove_event_detect(self._pin)
        subprocess.call(["sudo", "shutdown", "-h", "now"])

# --------------------------------------------------

    def shutdown_main(self):
        """Function that checks thet status of the shutdown pin to turn off the RPi"""

        previous_readings = []
        while len(previous_readings) < 4 or len(set(previous_readings)) > 1:
            reading = self.switch_shutdown.read_pin()
            previous_readings.append(reading)
            time.sleep(0.05)

        while True:
            time.sleep(0.05)
            reading = self.switch_shutdown.read_pin()
            previous_readings.append(reading)
            previous_readings = previous_readings[-5:]
            if len(set(previous_readings)) == 1 and reading == 1: # All readings are the same
                subprocess.call(["sudo", "shutdown", "-h", "now"])            

# --------------------------------------------------

if __name__ == "__main__":
    shutdown = Shutdown()
    shutdown.shutdown_main()
