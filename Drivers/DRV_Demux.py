# --------------------------------------------------

"""App that controls all the 74HC138 demultiplexers (active LOW)"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import RPi.GPIO as GPIO
import time
import APP_Config

# --------------------------------------------------

class Demux:
    """Demultiplexer functions"""

# --------------------------------------------------

    def __init__(self, Enable, Address):
        """Demultiplexer initialization"""
        
        GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins

        # Variables Initialization
        self._e0 = Enable[0]
        self._e1 = Enable[1]
        self._e2 = Enable[2]
        self._a0 = Address[0]
        self._a1 = Address[1]
        self._a2 = Address[2]

        # Pin Initialization
        GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
        GPIO.setwarnings(False)
        GPIO.setup(self._e0, GPIO.OUT) # Set Enable0 pin a output
        GPIO.setup(self._e1, GPIO.OUT) # Set Enable1 pin a output
        GPIO.setup(self._e2, GPIO.OUT) # Set Enable1 pin a output
        GPIO.setup(self._a0, GPIO.OUT) # Set Address0 pin a output
        GPIO.setup(self._a1, GPIO.OUT) # Set Address1 pin a output
        GPIO.setup(self._a2, GPIO.OUT) # Set Address2 pin a output

# --------------------------------------------------

    def signal(self, enable, address):
        """Function that lets you control the demultiplexer"""

        # Address
        GPIO.output(self._a0, address[0])
        GPIO.output(self._a1, address[1])
        GPIO.output(self._a2, address[2])

        # Enable
        GPIO.output(self._e0, enable[0])
        GPIO.output(self._e1, enable[1])
        GPIO.output(self._e2, enable[2])

# --------------------------------------------------

if __name__ == "__main__":
    #demux = Demux(APP_Config.PIN_D_M_ENABLE, APP_Config.PIN_D_M_ADDRESS)
    #demux.signal([False, False, False],[False, False, False])
    # Pin Initialization
    GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.OUT) # Set Enable0 pin a output
    GPIO.setup(19, GPIO.OUT) # Set Enable1 pin a output
    GPIO.setup(13, GPIO.OUT) # Set Enable1 pin a output

    while True:
        GPIO.output(26, True)
        time.sleep(1)
        GPIO.output(26, False)
        GPIO.output(19, True)
        time.sleep(1)
        GPIO.output(19, False)  
        GPIO.output(13, True)
        time.sleep(1)
        GPIO.output(13, False)
        time.sleep(1)
        GPIO.output(26, True)
        GPIO.output(19, True)
        GPIO.output(13, True)
        time.sleep(1)
        GPIO.output(26, False)
        GPIO.output(19, False)
        GPIO.output(13, False)

# --------------------------------------------------
