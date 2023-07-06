# --------------------------------------------------

"""Driver for HC_SR04 sensor control"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import time
import sys
import RPi.GPIO as GPIO

# --------------------------------------------------

# Global Variables

# Statuses
# Statuses
NONE = 0
GOOD = 1
OUT = 2
ERROR = 3

# --------------------------------------------------

# HC-SR04 class definition
class HCSR04:
    """HC-SR04 functions"""

# --------------------------------------------------

    def __init__(self, pin_sensor, maximum_distance, trigger_type=False, sample_number=1, interruptions=False, callback_start=None):
        """HC-SR04 initialization"""

        # Variable initialazation
        self._sound_speed = 343000 # Speed of Sound [m/s]
        self._max_dist = maximum_distance # Maximum scan distance [mm]
        self._max_dist_time = (1/self._sound_speed)*self._max_dist*2 #  Time it takes to send and receive a signal from the Maximum Distance
        self._max_dist_time_margin = self._max_dist_time*0.2
        self._timeout = (self._max_dist_time + self._max_dist_time_margin)/1000 # 20% extra error margin
        self._samples = sample_number # Number of samples used when averaging
        self._rest_time = 0.06 # Rest time between measurements suggested to avoid superposition [s]
        self._trigger_time = 0.0
        self._start_time = 0.0
        self._stop_time = 0.0
        self._time_elapsed = 0.0
        self._time_begin = 0.0
        self._status = NONE
        self._timeout_value = -1
        self._trigger_pin = 50
        self._sensor_pin = pin_sensor
        self._interruptions = interruptions
        self._callback_start = callback_start

        # Pin Initialization
        GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
        GPIO.setup(self._sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set Sensor pin as INPUT

        # Interrupts
        if self._interruptions is True:
            self._int_start()

# --------------------------------------------------

    def measure(self):
        """Function that emits a pulse, reads the answered value and returns the distance, with rest"""

        # Variable Reset
        self._status = NONE

        # Instructions
        self.trigger()
        value = self.read()
        distance = (value*self._sound_speed)/2
        time.sleep(self._rest_time)

        return distance

# --------------------------------------------------

    def measure_nr(self): # Measure with no Rest
        """Function that emits a pulse, reads the answered value and returns the distance, with no rest"""

        # Variable Reset
        self._status = NONE

        # Instructions
        self.trigger()
        value = self.read()
        if self._status is GOOD:
            distance = (value*self._sound_speed)/2
        else:
            distance = -1

        return distance

# --------------------------------------------------

    def measure_ntnr(self, trigger_time): # Measure with no Trigger and no Rest
        """Function that reads the answered value and returns the distance, with no rest"""

        # Variable Reset
        self._status = NONE

        # Trigger Times
        self._trigger_time = trigger_time

        # Instructions
        value = self.read()
        if self._status == GOOD:
            distance = (value*self._sound_speed)/2
        else:
            distance = value

        return distance

# --------------------------------------------------

    def measure_ntntnr(self): # Measure with no Trigger, no Trigger Time and no Rest
        """Function that reads the answered value and returns the distance, with no rest"""

        # Variable Reset
        self._status = NONE

        # Instructions
        value = self.read_nt()
        if self._status == GOOD:
            distance = (value*self._sound_speed)/2
        else:
            distance = value

        return distance

# --------------------------------------------------

    def measure_ntntnr_long(self): # Measure with no Trigger, no Trigger Time and no Rest
        """Function that reads the answered value and returns the distance, with no rest"""

        # Variable Reset
        self._status = NONE

        # Instructions
        value = self.read_nt_long()
        if self._status == GOOD:
            distance = (value*self._sound_speed)/2
        else:
            distance = value

        return distance
# --------------------------------------------------

    def measure_and_avg(self):
        """Function that emits a pulse, reads the answered value, takes an amount of 'samples' and averages them"""

        # Variable Reset
        useful = 0
        self._status = NONE

        # Instructions
        counter_maa = 1
        value_tot = 0
        while counter_maa <= self._samples:
            while self._status != GOOD:
                self.trigger()
                value = self.read()
                time.sleep(self._rest_time)
            useful = useful + 1
            value_tot = value_tot + value
            counter_maa = counter_maa + 1

        value_avg = value_tot/self._samples
        distance = (value_avg*self._sound_speed)/2

        return distance

# --------------------------------------------------

    def trigger(self):
        """Sub-function that emits a pulse through the trigger pin"""

        # 10us pulse in Trigger
        GPIO.output(self._trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self._trigger_pin, False)

        # Time when the Trigger was sent
        self._trigger_time = time.monotonic()

# --------------------------------------------------

    def read(self):
        """"Sub-fuction that reads the sensors"""

        # Variables reset
        timeout_1 = False
        timeout_2 = False
        self._start_time = 0.0
        self._stop_time = 0.0
        self._time_elapsed = 0.0
        self._time_begin = 0.0

        # Beginning Time
        self._time_begin = time.monotonic()

        # Get the first time stamp before rising edge
        while GPIO.input(self._sensor_pin) == 0:
            self._start_time = time.monotonic()
            if (time.monotonic()-self._time_begin) > 0.0026: #10*self._timeout:
                timeout_1 = True
                break

        # Get the last time stamp before falling edge
        if timeout_1 is False and timeout_2 is False:
            while GPIO.input(self._sensor_pin) == 1:
                self._stop_time = time.monotonic()
                if (time.monotonic()-self._trigger_time) > 0.0026: #10*self._timeout:
                    timeout_2 = True
                    break

        if timeout_1 is True or timeout_2 is True:
            # Out of range measurement
            self._time_elapsed = self._timeout_value 
            self._status = OUT
        elif timeout_1 is False and timeout_2 is False:
            # Calculate pulse length.
            self._time_elapsed = self._stop_time - self._start_time
            if self._time_elapsed > 0.0 and self._time_elapsed <= self._timeout:
                self._status = GOOD
            else:
                self._time_elapsed = -10
                self._status = ERROR

        return self._time_elapsed

# --------------------------------------------------

    def read_nt(self):
        """"Sub-fuction that reads the sensors"""
        # Variables reset
        timeout_1 = False
        timeout_2 = False
        self._status = GOOD
        self._start_time = 0.0
        self._stop_time = 0.0
        self._time_elapsed = 0.0
        self._time_begin = 0.0

        # Beginning Time
        self._time_begin = time.monotonic()

        # Get the first time stamp before rising edge
        while GPIO.input(self._sensor_pin) == 0:
            self._start_time = time.monotonic()
            if (time.monotonic()-self._time_begin) > 0.0035: #10*self._timeout:    0.0013
                timeout_1 = True
                break

        # Get the last time stamp before falling edge
        if timeout_1 is False:
            while GPIO.input(self._sensor_pin) == 1:
                self._stop_time = time.monotonic()
                if (time.monotonic()-self._time_begin) > 0.0035: #10*self._timeout:    0.0013
                    timeout_2 = True
                    break

        if timeout_1 is True or timeout_2 is True:
            # Out of range measurement
            self._time_elapsed = self._timeout_value 
            self._status = OUT
        elif timeout_1 is False and timeout_2 is False:
            # Calculate pulse length.
            self._time_elapsed = self._stop_time - self._start_time
            if self._time_elapsed > 0.0: # and self._time_elapsed <= 2*self._timeout:
                self._status = GOOD
            else:
                self._time_elapsed = -10
                self._status = ERROR
                
        return self._time_elapsed


# --------------------------------------------------

    def read_nt_long(self):
        """"Sub-fuction that reads the sensors"""
        # Variables reset
        timeout_1 = False
        timeout_2 = False
        self._status = GOOD
        self._start_time = 0.0
        self._stop_time = 0.0
        self._time_elapsed = 0.0
        self._time_begin = 0.0

        # Beginning Time
        self._time_begin = time.monotonic()

        # Get the first time stamp before rising edge
        while GPIO.input(self._sensor_pin) == 0:
            self._start_time = time.monotonic()
            if (time.monotonic()-self._time_begin) > 0.004: #10*self._timeout:   0.0023
                timeout_1 = True
                break

        # Get the last time stamp before falling edge
        if timeout_1 is False:
            while GPIO.input(self._sensor_pin) == 1:
                self._stop_time = time.monotonic()
                if (time.monotonic()-self._time_begin) > 0.004: #10*self._timeout:   0.0023
                    timeout_2 = True
                    break

        if timeout_1 is True or timeout_2 is True:
            # Out of range measurement
            self._time_elapsed = self._timeout_value 
            self._status = OUT
        elif timeout_1 is False and timeout_2 is False:
            # Calculate pulse length.
            self._time_elapsed = self._stop_time - self._start_time
            if self._time_elapsed > 0.0: # and self._time_elapsed <= 2*self._timeout:
                self._status = GOOD
            else:
                self._time_elapsed = -10
                self._status = ERROR
                
        return self._time_elapsed

# --------------------------------------------------

    def value_to_distance(self, value):
        """Function that converts the time measurement to the distance measured"""
        distance = (value*self._sound_speed*1000)/2
        return distance

# --------------------------------------------------

    def _int_start(self):
        """Function that configures an interruption on the rising edge of the echo"""
        if self._callback_start is None:
            GPIO.add_event_detect(self._sensor_pin, GPIO.RISING, callback=self.cb_int_start, bouncetime=1)
        else:
            GPIO.add_event_detect(self._sensor_pin, GPIO.RISING, callback=self._callback_start, bouncetime=1)

# --------------------------------------------------

    def cb_int_start(self):
        """Callback on the rising edge of the echo"""
        self._start_time = time.monotonic()

        while GPIO.input(self._sensor_pin) == GPIO.HIGH:
            self._stop_time = time.monotonic()

# --------------------------------------------------

    def stop(self):
        """Function that stops the HC-SR04 sensors"""

        # Reset GPIO
        GPIO.cleanup()

# --------------------------------------------------

#if __name__ == "__main__":
#    hcsr04 = [HCSR04(APP_Config.PIN_TRIGGER[0], APP_Config.PIN_SENSOR[0], APP_Config.MAXIMUM_DISTANCE),
#              HCSR04(APP_Config.PIN_TRIGGER[1], APP_Config.PIN_SENSOR[1], APP_Config.MAXIMUM_DISTANCE)]

#    # Database Initialization
#    db = Database()

#    while True:
#        for counter in range(len(APP_Config.PIN_SENSOR)):
#            value_0 = hcsr04[counter].measure_nr()
#            db.update_value(counter, round(value_0, 2))
#            value_1 = db.select_value(counter)
#            print('Sensor {} - {} mm'.format(counter, round(value_0, 2)))
#            print('Sensor {} - {} mm'.format(counter, value_1[0]))
#            sys.stdout.flush()
#            time.sleep(2)

# --------------------------------------------------
