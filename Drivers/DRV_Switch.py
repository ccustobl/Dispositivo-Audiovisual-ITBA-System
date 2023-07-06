#!/usr/bin/env python3

# --------------------------------------------------

"""Driver to control the Switches on the front panel"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import RPi.GPIO as GPIO
import APP_Config
import sys
import time
from functools import partial

# --------------------------------------------------

class Switch:
    """Switch Functions"""

# --------------------------------------------------

    def __init__(self, pin_switch, new_callback=False, mycallback=None, *args):
        """Initialization"""

        # Pin Initizalization
        self._pin = pin_switch
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Interruption setup        
        #if mycallback is None:
        #        mycallback = self._cb_change
        #if new_callback is False:
        #    callback = partial(self._cb_change, *args)
        #    GPIO.add_event_detect(self._pin, GPIO.BOTH, callback, bouncetime=300)
        #else:
        #    callback = partial(mycallback, *args)
        #    GPIO.add_event_detect(self._pin, GPIO.BOTH, callback, bouncetime=300)

# --------------------------------------------------

    def read_pin(self):
        """Function that reads the status of the pin"""

        pin_status = GPIO.input(self._pin)
        return pin_status

# --------------------------------------------------

    def _cb_change(self, *args):
        """Callback on the change of status of the switch"""
        #if GPIO.input(self._pin):
        #    print("Switch is closed.")
        #    sys.stdout.flush()
        #else:
        #    print("Switch is open.")
        #    sys.stdout.flush()
        print(GPIO.input(self._pin))
        sys.stdout.flush()

# --------------------------------------------------

if __name__ == "__main__":
    #switch = Switch()

    #while True:
    #    pass

    # Test 0
    # set up GPIO numbering mode and define pins for the switches
    #GPIO.setmode(GPIO.BCM)
    #switch1_pin = 11 #APP_Config.PIN_SWITCH[0]
    #switch2_pin = 9 #APP_Config.PIN_SWITCH[1]
    #switch3_pin = 10 #APP_Config.PIN_SWITCH[2]

    # set up the switch pins as inputs and enable internal pull-up resistors
    #GPIO.setup(switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(switch3_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(switch3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)   

    #print('Done')
    #counter=0

    # loop to continuously read the switch states and print the results
    #while True:
        # read the state of each switch and print the results
    #    switch1_state = GPIO.input(switch1_pin)
    #    switch2_state = GPIO.input(switch2_pin)
    #    switch3_state = GPIO.input(switch3_pin)
    #    print(counter)
    #    sys.stdout.flush()
    #    print(f"Switch 1 state: {switch1_state}")
    #    sys.stdout.flush()
    #    print(f"Switch 2 state: {switch2_state}")
    #    sys.stdout.flush()
    #    print(f"Switch 3 state: {switch3_state}")
    #    sys.stdout.flush()

        #if switch1_state==1 or switch2_state==1 or switch3_state==1:
        #    print('Funciona')
    #    counter+=1
        # wait a short time before reading the switches again
    #    time.sleep(1)

    # Test 1
    switch0 = Switch(APP_Config.PIN_SWITCH[0], False, None)
    switch1 = Switch(APP_Config.PIN_SWITCH[1], False, None)
    print('Done')
    #for x in range(5):
    #    switch1_state = GPIO.input(APP_Config.PIN_SWITCH[0])
    #    print(f"Switch 1 state: {switch1_state}")
    #    time.sleep(1)
    while True:
        pass
