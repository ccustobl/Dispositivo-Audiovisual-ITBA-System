# --------------------------------------------------

"""Driver for Hardware PWM control"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import RPi.GPIO as GPIO

# --------------------------------------------------

# LED class definition
class PWM_HW:
    """PWM_HW functions"""

# --------------------------------------------------

    def __init__(self, pin_pwm, pwm_freq):
        """PWM initialization"""

        # Variable initialization
        self._pwm_pin = pin_pwm
        self._freq = pwm_freq

        # Pin initialization
        GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
        GPIO.setup(self._pwm_pin, GPIO.OUT) # Set PWM pin as OUTPUT

        # PWM initialization
        self._pwm = GPIO.PWM(self._pwm_pin, self._freq)
        self._pwm.ChangeDutyCycle(0)

# --------------------------------------------------

    def shine(self, duty_cycle):
        """PWM duty cycle control"""

        self._pwm.ChangeDutyCycle(duty_cycle)

# --------------------------------------------------
