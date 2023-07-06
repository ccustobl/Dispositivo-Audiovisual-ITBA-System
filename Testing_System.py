# --------------------------------------------------

"""App that controls all the HC-SR04 ultrasonic sensors"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import time
import sys
import RPi.GPIO as GPIO
from Drivers.DRV_HCSR04 import HCSR04
from Drivers.DRV_Data_Sensor import Database_Sensor
from Drivers.DRV_Demux import Demux
import APP_Config

# --------------------------------------------------

# Defines
Demux_OFF = [[False, False, False], ]
Demux_Enable = [[True, False, False],
                [False, True, False],
                [False, False, True]]
Demux_Address = [[False, False, False,],
                 [False, False, True,],
                 [False, True, False,],
                 [False, True, True,],
                 [True, False, False,],
                 [True, False, True,],
                 [True, True, False,],
                 [True, True, True,]]

# --------------------------------------------------

# All ultrasonic sensors control
class Testing_System:
    """Ultrasonic sensors functions"""

# --------------------------------------------------

    def __init__(self):
        """Ultrasonic initialization"""

        # Variables Initialization
        self._sensor_number = 15
        self._pin_in_use = 0
        self._distance = 0
        self._start_time = 0.0
        #self._time_sleep = 0.05 / self._sensor_number
        #self._time_sleep = 0.003125
        self._time_sleep = 0.01
        self._previous = [0] * 16

        # Database Initialization
        self.db = Database_Sensor()
        self.database_reset()

        # Demultiplexer Intialization
        self.demux = Demux(APP_Config.PIN_D_M_ENABLE, APP_Config.PIN_D_M_ADDRESS)
        self.demux.signal(Demux_Enable[0], Demux_Address[7])

        # Sensor Initialization
        #self.hcsr04 = [HCSR04(APP_Config.PIN_SENSOR[0], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[1], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[2], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[3], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[4], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[5], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[6], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[7], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[8], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[9], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[10], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[11], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[12], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[13], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[14], APP_Config.MAXIMUM_DISTANCE),
        #               HCSR04(APP_Config.PIN_SENSOR[15], APP_Config.MAXIMUM_DISTANCE)]

        self.hcsr04 = [HCSR04(APP_Config.PIN_SENSOR[0], APP_Config.MAXIMUM_DISTANCE)]

# --------------------------------------------------

    def test(self):
        """Main function"""
        
        GPIO.setup(APP_Config.PIN_SENSOR[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set Sensor pin as INPUT

        sensor_number = 8
        counter_enable = 0
        counter_address = 0

        values = [0]*sensor_number
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} |'.format(*range(sensor_number)))

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        time.sleep(0.5)

        while True:
            for counter_general in range(sensor_number):

                if counter_general == 0:
                    time_start_loop = time.monotonic()

                start_time = 0.0
                stop_time = 0.0
                # Demux Address and Enable Selection, Demux Trigger
                self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])

                time_begin = time.monotonic()

                # Get the first time stamp before rising edge
                while GPIO.input(APP_Config.PIN_SENSOR[0]) == 0:
                    start_time = time.monotonic()
                    if (time.monotonic()-time_begin) > 0.005:
                        start_time = 0.0
                        break

                # Get the last time stamp before falling edge
                while GPIO.input(APP_Config.PIN_SENSOR[0]) == 1:
                    stop_time = time.monotonic()
                    if (time.monotonic()-time_begin) > 0.005:
                        stop_time = 0.0
                        break

                elapsed_time = stop_time - start_time
                self._distance = (elapsed_time*343000)/2

                if self._distance < 0:
                    self._distance = -100

                if self._distance > 1000:
                    self._distance = -1

                values[counter_general] = self._distance

                # Counter Management
                counter_general = counter_general + 1
                counter_address = counter_address + 1                

                if counter_general == sensor_number:
                    counter_address = 0
                    counter_general = 0

                    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} |'.format(*values))
                    sys.stdout.flush()

                    time_end_loop = time.monotonic()

                    time_loop = time_end_loop-time_start_loop
                    #print(time_loop)
                    sys.stdout.flush()

                # Wait
                time.sleep(0.0005)

# --------------------------------------------------

    def cb_hcsr04_start(self):
        """Callback for the Rising Edge of the echo"""
        self._start_time = time.monotonic()

# --------------------------------------------------

    def database_setup(self):
        """Function that creates the sensor database"""

        self.db.create_table()

        for counter in range(len(APP_Config.PIN_SENSOR)):
            self.db.create_row(APP_Config.PIN_SENSOR[counter], -1)

# --------------------------------------------------

    def database_reset(self):
        """Function that resets the values in the sensor database"""

        for counter in range(len(APP_Config.PIN_SENSOR)):
            self.db.update_value(APP_Config.PIN_SENSOR[counter], -1)

# --------------------------------------------------

if __name__ == "__main__":

    GPIO.cleanup()
    sys.stdout.flush()
    test_sys = Testing_System()

    test_sys.test()