# --------------------------------------------------

"""Driver for Software PWM control"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import RPi.GPIO as GPIO
import time

# --------------------------------------------------

# LED class definition
class PWM_SW:
    """PWM_SW functions"""

# --------------------------------------------------

    def __init__(self, pin_pwm):
        """PWM initialization"""

        # Variable Initialization
        self._pwm_pin = pin_pwm

        # Pin initialization
        GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
        GPIO.setup(self._pwm_pin, GPIO.OUT) # Set PWM pin as OUTPUT

# --------------------------------------------------

    def pwm_on(self):
        """Function that sends a 1 to the PWM Pin"""
        GPIO.output(self._pwm_pin, True)

# --------------------------------------------------

    def pwm_off(self):
        """Function that sends a 0 to the PWM Pin"""
        GPIO.output(self._pwm_pin, False)

# --------------------------------------------------

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
    GPIO.setup(17, GPIO.OUT) # Set PWM pin as OUTPUT
    GPIO.setup(27, GPIO.OUT) # Set PWM pin as OUTPUT
    GPIO.setup(22, GPIO.OUT) # Set PWM pin as OUTPUT


    while True:
        GPIO.output(17, True)
        GPIO.output(27, True)
        GPIO.output(22, True)
        time.sleep(1)
        GPIO.output(17, False)
        GPIO.output(27, False)
        GPIO.output(22, False)
        time.sleep(1)

