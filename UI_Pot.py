# --------------------------------------------------

"""APP for Potentiometer Control"""
# Author: Custo Blanch, Christian
# ITBA

# --------------------------------------------------

# Imports

import time
import sys
from functools import partial
from Drivers.DRV_Data_Pot import Database_Pot
from Drivers.DRV_Data_LED import Database_LED
from Drivers.DRV_ADC import ADC
import APP_Config

# --------------------------------------------------
class Potentiometer():
    """Potentiometer functions"""

# --------------------------------------------------

    def  __init__(self, mycallback, *args):
        """Initialization"""
        # Constant initialization
        #self.step_1 = 52.54 # ((APP_Config.POT_MAX_VALUE - APP_Config.POT_MIN_VALUE)/((10/1)/2))/100 = 52.54
        #self.step_1 = 105.08 # ((APP_Config.POT_MAX_VALUE - APP_Config.POT_MIN_VALUE)/((10/2)/2))/100 = 105.08
        self.step_1 = 131.35 # ((APP_Config.POT_MAX_VALUE - APP_Config.POT_MIN_VALUE)/((10/3)/2))/100 = 131.35
        self.range = self.step_1*100
        self.extreme_margin = self.step_1*10
        self.margin = 17 # To avoid meassurement errors
        self.lower_limit = APP_Config.POT_MIN_VALUE + self.extreme_margin  # self.range
        self.upper_limit = APP_Config.POT_MAX_VALUE - self.extreme_margin  # self.range
        self.upper_max = APP_Config.POT_MAX_VALUE

        # Variable initialization
        self._duty_old = 0
        self._check_extremes = [False, False, False, False]

        # ADC Initialization
        self.adc = ADC(APP_Config.ADDRESS_1)

        # Database Inititialization
        self.db_pot = Database_Pot()
        self.db_led = Database_LED()
        self.database_reset()

        # Callback Initialization
        self.callback = partial(mycallback, *args)

# --------------------------------------------------

    def ui_pot_main(self):
        """Potentiometers main loop"""
        values = [0]*4
        olds = [0]*4
        while True:
            for i in range(4):
                # Read ADC
                value = self.adc.adc_read(i)

                # Get Variables Ready
                values[i] = value
                old = self.db_pot.select_value_col2(i)
                olds [i] = old

                # Check if theres a change in Potentiometer
                if old-value >= self.margin: # there was a substantial anti-clockwise rotation
                    self._duty_old = self.db_led.select_value(i)
                    self.duty_cycle_calc_minus(i, old-value, value)
                    self.db_pot.update_value_col1(i, value)
                    self.db_pot.update_value_col2(i, value)
                    # Verify Extremes
                    #self.check_extremes(i, value)
                elif value-old >= self.margin: # there was a substantial clockwise rotation
                    self._duty_old = self.db_led.select_value(i)
                    self.duty_cycle_calc_plus(i, value-old, value)
                    self.db_pot.update_value_col1(i, value)
                    self.db_pot.update_value_col2(i, value)
                    # Verify Extremes
                    #self.check_extremes(i, value)
            #print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} ||'.format(*values))
            #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6}  |'.format(*values))
            sys.stdout.flush()
            time.sleep(0.5)

# --------------------------------------------------

    def database_reset(self):
        """Function that resets the values in the sensor database"""
        for counter in range(len(APP_Config.POTS)):
            self.db_pot.update_value_col1(APP_Config.POTS[counter], 0)
            self.db_pot.update_value_col2(APP_Config.POTS[counter], 0)

# --------------------------------------------------

    def duty_cycle_calc_plus(self, pos, new_dif, new_meassurement):
        """Function that calculates the duty cycle that corresponds to the ADC reading"""
        if self._duty_old < 100:
            new_duty = self._duty_old + new_dif/self.step_1
            if new_duty >= 100 or new_meassurement > self.upper_limit:
                new_duty = 100
            #print("plus")
            #print(pos)
            #print(new_duty)
            #sys.stdout.flush()
            self.callback(pos, new_duty)

# --------------------------------------------------

    def duty_cycle_calc_minus(self, pos, new_dif, new_meassurement):
        """Function that calculates the duty cycle that corresponds to the ADC reading"""
        if self._duty_old > 0:
            new_duty = self._duty_old - new_dif/self.step_1
            if new_duty <= 0 or new_meassurement < self.lower_limit:
                new_duty = 0
            #print("minus")
            #print(pos)
            #print(new_duty)
            #sys.stdout.flush()
            self.callback(pos, new_duty)

# --------------------------------------------------

    def check_extremes(self, pos, new_meassurement):
        """Function that verifies the User has room to increase or lower the LED duty dycle"""
        # Verify lower extreme
        if new_meassurement < self.lower_limit: # Lower Extreme
            new_duty = 0
            self.callback(pos, new_duty)
            #print("extreme")
            #print(pos)
            #print(new_duty)
            #sys.stdout.flush()
        elif new_meassurement > self.upper_limit: # Upper Extreme
            new_duty = 100
            self.callback(pos, new_duty)
            #print("extreme")
            #print(pos)
            #print(new_duty)
            #sys.stdout.flush()
        self._check_extremes[pos] = False

# --------------------------------------------------

    def check_extremes_cb(self, *args):
        """Function that raises the flag to check extremes"""
        self._check_extremes = [True, True, True, True]
        print("extreme cb")
        sys.stdout.flush()

# --------------------------------------------------
