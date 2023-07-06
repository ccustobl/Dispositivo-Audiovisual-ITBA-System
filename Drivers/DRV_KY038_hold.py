# --------------------------------------------------

"""Driver to control the KY-038"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import time
import RPi.GPIO as GPIO
from Drivers.DRV_Data_Mic import Database_Mic

# --------------------------------------------------

# KY038 Class Definition
class KY038:
    """KY-038 Functions"""

# --------------------------------------------------

    def __init__(self, pin_mic_digital, pin_mic_analog=41, select_digital=True, new_callback=False, mycallback=None):
        """KY-038 initialization"""

        # Variable Initialization
        self._pin_mic_digital = pin_mic_digital
        self._pin_mic_analog = pin_mic_analog
        self._start_digital_time = 0.0
        self._stop_digital_time = 0.0
        self._duration = -1

        # Pin Initialization
        GPIO.setmode(GPIO.BCM)
        if select_digital is True:
            GPIO.setup(self._pin_mic_digital, GPIO.IN)
        elif select_digital is False:
            GPIO.setup(self._pin_mic_analog, GPIO.IN)

        # Database
        self.db_mic = Database_Mic()

        # Interruption setup
        if new_callback is False:
            GPIO.add_event_detect(self._pin_mic_digital, GPIO.RISING, self._cb_int_digital, bouncetime=300)
        else:
            GPIO.add_event_detect(self._pin_mic_digital, GPIO.RISING, mycallback, bouncetime=300)

# --------------------------------------------------

    def _cb_int_digital(self):
        """Callback on the rising edge of the echo"""

        # Get the first time stamp of the rising edge
        self._start_digital_time = time.monotonic()

        # Get the last time stamp before falling edge
        while GPIO.input(self._pin_mic_digital) == 1:
            self._stop_digital_time = time.monotonic()

        self._duration = self._stop_digital_time - self._start_digital_time
        self.db_mic.update_value(0, 1)
        self.db_mic.update_value(1, self._duration)

# --------------------------------------------------

#if __name__ == "__main__":
#    def cb(self):
#        print("clap")
#        sys.stdout.flush()
#    ky038 = KY038(APP_Config.PIN_KY038_DIG, 0, True, True, cb)
#    while True:
#        time.sleep(10)

# --------------------------------------------------
