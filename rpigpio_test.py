# --------------------------------------------------

"""App to test RPiGPIO"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import RPi.GPIO as GPIO
import time

# --------------------------------------------------

if __name__ == "__main__":
    
    #GPIO.cleanup()
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)

    #GPIO.setup(4, GPIO.OUT) # Set pin as output    

    #while True:
    #    GPIO.output(4, True)
    #    time.sleep(1)
    #    GPIO.output(4, False)
    #    time.sleep(1)
    #
    #    GPIO.cleanup()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT) # Set pin as output
    GPIO.setup(27, GPIO.OUT) # Set pin as output
    GPIO.setup(22, GPIO.OUT) # Set pin as output

    while True:
        GPIO.output(17, True)
        GPIO.output(27, False)
        GPIO.output(22, False)
        time.sleep(1)
        GPIO.output(17, False)
        GPIO.output(27, True)
        GPIO.output(22, False)
        time.sleep(1)
        GPIO.output(17, False)
        GPIO.output(27, False)
        GPIO.output(22, True)
        time.sleep(1)

# --------------------------------------------------