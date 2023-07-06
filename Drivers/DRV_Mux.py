# --------------------------------------------------

"""App that controls all the 74LS151 multiplexers"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import time
import RPi.GPIO as GPIO

# --------------------------------------------------

# Global Variables

# Statuses
NONE = 0
GOOD = 1
OUT = 2
ERROR = 3

# --------------------------------------------------

class Mux:
    """Multiplexer functions"""

# --------------------------------------------------

    def __init__(self, Enable, Address, maximum_distance):
        """Multiplexer initialization"""
        # Variables Initialization
        self._e0 = Enable[0]
        self._e1 = Enable[1]
        self._e2 = Enable[2]
        self._e = Enable
        self._a0 = Address[0]
        self._a1 = Address[1]
        self._a2 = Address[2]

        self._sound_speed = 343 # Speed of Sound [m/s]
        self._max_dist = maximum_distance # Maximum scan distance [mm]
        self._max_dist_time = (1/self._sound_speed)*self._max_dist*2 #  Time it takes to send and receive a signal from the Maximum Distance
        self._max_dist_time_margin = self._max_dist_time*0.1
        self._timeout = (self._max_dist_time + self._max_dist_time_margin)/1000 # 10% extra error margin
        self._rest_time = 0.06 # Rest time between measurements suggested to avoid superposition [s]
        self._trigger_time = 0.0
        self._start_time = 0.0
        self._stop_time = 0.0
        self._time_elapsed = 0.0
        self._status = NONE

        # Pin Initialization
        GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
        GPIO.setup(self._e0, GPIO.OUT) # Set Enable0 pin a output
        GPIO.setup(self._e1, GPIO.OUT) # Set Enable1 pin a output
        GPIO.setup(self._e2, GPIO.OUT) # Set Enable2 pin a output
        GPIO.setup(self._a0, GPIO.OUT) # Set Address0 pin a output
        GPIO.setup(self._a1, GPIO.OUT) # Set Address1 pin a output
        GPIO.setup(self._a2, GPIO.OUT) # Set Address2 pin a output

# --------------------------------------------------

    def change_receive(self, enable_nmbr, address):
        """Function that lets you control the multiplexer"""

        # Address
        GPIO.output(self._a0, address[0])
        GPIO.output(self._a1, address[1])
        GPIO.output(self._a2, address[2])

        # Enable
        GPIO.output(self._e[enable_nmbr], True)

# --------------------------------------------------

    def read_mux(self, trigger_time):
        """Function that reads the value answered value and returns the distance"""


# --------------------------------------------------

# if __name__ == "__main__":
#     mux = Mux(APP_Config.PIN_D_M_ENABLE, APP_Config.PIN_D_M_ADDRESS)
#     mux.receive(0, [True, True, True])
#     time.sleep(20)
#     GPIO.cleanup()

# --------------------------------------------------
