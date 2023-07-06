# --------------------------------------------------

"""APP for Piezometric Sensor Control"""
# Author: Custo Blanch, Christian
# ITBA

# --------------------------------------------------

# Imports

import time
import sys
import RPi.GPIO as GPIO
from Drivers.DRV_ADC import ADC
import APP_Config

# --------------------------------------------------
class Piezo():
    """Piezometric Sensor functions"""

# --------------------------------------------------

    def  __init__(self):
        """Initialization"""
        # Constant initialization


        # Variable initialization

        # ADC Initialization
        self.adc = ADC(APP_Config.ADDRESS_2)
        # self.adc.adc_start_cont(self, channel, high_thresh, low_thresh):

        # Alert setup
        self._pin = APP_Config.PIN_ADC_ALERT
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Database Inititialization
        # self.db_led = Database_LED()
        # self.database_reset()

        # Callback Initialization
        #self.callback = partial(mycallback, *args)

        # Sleep
        time.sleep(1)

# --------------------------------------------------

    def ui_piezo_main(self):
        """Potentiometers main loop"""
        #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        #print('-' * 37)
        self.adc.adc_start_cont(0, 4000000, -4000000)
        time.sleep(1)
        while True:
            #print(GPIO.input(self._pin))
            if GPIO.input(self._pin) == 1:
                print(GPIO.input(self._pin))
                # Read ADC
                value = self.adc.adc_get_value()
                print('Channel 0: {0}'.format(value))
                sys.stdout.flush()

            time.sleep(0.1)
 
# --------------------------------------------------

    def test1(self):
        """Potentiometers main loop"""
        values = [0]*4
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        print('-' * 37)
        while True:
            for i in range(4):
                # Read ADC
                values[i] = self.adc.adc_read(i)

            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
            sys.stdout.flush()

            time.sleep(0.5)

# --------------------------------------------------

    def database_reset(self):
        """Function that resets the values in the potentiometer database"""
        for counter in range(len(APP_Config.POTS)):
            self.db_pot.update_value_col1(APP_Config.POTS[counter], 0)
            self.db_pot.update_value_col2(APP_Config.POTS[counter], 0)

# --------------------------------------------------

if __name__ == "__main__":
    piezo = Piezo()
    piezo.ui_piezo_main()

# --------------------------------------------------
