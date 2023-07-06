# --------------------------------------------------

"""App that controls LEDs using Software PWM"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import sys
import time
import threading
import multiprocessing as mp
import APP_Config
from Drivers.DRV_PWM_SW import PWM_SW
from Drivers.DRV_Data_LED import Database_LED

# --------------------------------------------------

# LED Initialization
class LED_SW():
    """LED Software PWM functions"""

# --------------------------------------------------

    def __init__(self, led, pos, freq):
        """LEDs initialization"""

        # Variable Initialization
        self._period = 1/float(freq)
        self._pulse_width_on = 0
        self._pulse_width_off = 0.001
        self._duty_cycle = 50
        self._pulse_on = 0
        self._pulse_off = 0.001
        self._led = led
        self._pos = pos
        self._pwm_counter = 150
        self._mode = 0

        # Database Inititialization
        self.db = Database_LED()

        # Shared Memory
        self.shared_var_on = mp.Value('d', self._pulse_width_on)
        self.shared_var_off = mp.Value('d', self._pulse_width_off)
        self.shared_var_mode = mp.Value('i', self._mode)

        # Threading PWM
        #led_pwm_thread = threading.Thread(target=self.led_pwm, args=(self.shared_var_on, self.shared_var_off, self.shared_var_mode))
        #led_pwm_thread.start()

        # Multiprocessing
        pwm_process = mp.Process(target=self.led_pwm_new, args=(self._led, self.shared_var_on, self.shared_var_off, self.shared_var_mode))
        pwm_process.start()

# --------------------------------------------------


    def led_pwm_new(self, _led, shared_var_on, shared_var_off, shared_var_mode):
        """LEDs PWM Software Loop Function"""

        # LED class initialization
        pwm_sw = PWM_SW(_led)
        pwm_sw.pwm_off()

        # Loop
        while True:
            if self._pwm_counter >= 100:
                # Copy width values                
                self._pulse_on = shared_var_on.value
                self._pulse_off = shared_var_off.value
                self._mode = shared_var_mode.value
                self._pwm_counter = 0
                #print(self._mode)  
                #print(self._pulse_on)
                #print(self._pulse_off)  
                #sys.stdout.flush()  

            # PWM
            if self._mode == 0:
                while self._pwm_counter < 100:
                    pwm_sw.pwm_off()
                    time.sleep(self._pulse_off)
                    # Counter Management
                    self._pwm_counter += 1

            elif self._mode == 1:
                while self._pwm_counter < 100:
                    pwm_sw.pwm_on()
                    time.sleep(self._pulse_on)
                    # Counter Management
                    self._pwm_counter += 1

            elif self._mode == 2:
                while self._pwm_counter < 100:
                    pwm_sw.pwm_on()
                    time.sleep(self._pulse_on)
                    pwm_sw.pwm_off()
                    time.sleep(self._pulse_off)
                    # Counter Management
                    self._pwm_counter += 1

# --------------------------------------------------

    def led_pwm(self, shared_var_on, shared_var_off, shared_var_mode):
        """LEDs PWM Software Loop Function"""

        # LED class initialization
        self.pwm_sw = PWM_SW(self._led)

        # Loop
        while True:
            if self._pwm_counter >= 100:
                # Copy width values                
                self._pulse_on = shared_var_on.value
                self._pulse_off = shared_var_off.value
                self._mode = shared_var_mode.value
                self._pwm_counter = 0

            # PWM
            if self._mode == 0:
                while self._pwm_counter < 100:
                    self.pwm_sw.pwm_off()
                    time.sleep(self._pulse_off)
                    # Counter Management
                    self._pwm_counter = self._pwm_counter + 1

            elif self._mode == 1:
                while self._pwm_counter < 100:
                    self.pwm_sw.pwm_on()
                    time.sleep(self._pulse_on)
                    # Counter Management
                    self._pwm_counter = self._pwm_counter + 1

            elif self._mode == 2:
                while self._pwm_counter < 100:
                    self.pwm_sw.pwm_on()
                    time.sleep(self._pulse_on)
                    self.pwm_sw.pwm_off()
                    time.sleep(self._pulse_off)
                    # Counter Management
                    self._pwm_counter = self._pwm_counter + 1

# --------------------------------------------------

    def pwm_calc(self, duty_cycle):
        """Function that calculates the ON and OFF times of the PWM"""

        self._duty_cycle = duty_cycle
        #self._pulse_width_on = self._duty_cycle / float(100) * self._period
        #self._pulse_width_off = self._period - self._pulse_width_on
        if self._duty_cycle == 0:
            self._pulse_width_on = 0
            self._pulse_width_off = self._period
            with self.shared_var_on.get_lock():
                self.shared_var_on.value = self._pulse_width_on
            with self.shared_var_off.get_lock():
                self.shared_var_off.value = self._pulse_width_off
            with self.shared_var_mode.get_lock():
                self.shared_var_mode.value = 0
            #print(self._pulse_width_on)
            #print(self._pulse_width_off)
            #sys.stdout.flush()

        elif self._duty_cycle == 100:
            self._pulse_width_on =  self._period
            self._pulse_width_off = 0
            with self.shared_var_on.get_lock():
                self.shared_var_on.value = self._pulse_width_on
            with self.shared_var_off.get_lock():
                self.shared_var_off.value = self._pulse_width_off
            with self.shared_var_mode.get_lock():
                self.shared_var_mode.value = 1
            #print(self._pulse_width_on)
            #print(self._pulse_width_off)
            #sys.stdout.flush()

        else:
            self._pulse_width_on = self._duty_cycle / float(100) * self._period
            self._pulse_width_off = self._period - self._pulse_width_on
            with self.shared_var_on.get_lock():
                self.shared_var_on.value = self._pulse_width_on
            with self.shared_var_off.get_lock():
                self.shared_var_off.value = self._pulse_width_off
            with self.shared_var_mode.get_lock():
                self.shared_var_mode.value = 2
            #print(self._pulse_width_on)
            #print(self._pulse_width_off)
            #sys.stdout.flush()  

# --------------------------------------------------

    def test(self):
        """Function for Testing"""

        # Begin calculation
        pwm_calc_thread = threading.Thread(target=self.pwm_calc, args=())
        pwm_calc_thread.start()

        while True:
            time.sleep(10)
            print(900)
            sys.stdout.flush()
            self.db.update_value(self._pos, 99)
            #self._pulse_width_on = 0.5
            #self._pulse_width_off = 0.5
            time.sleep(20)
            print(500)
            sys.stdout.flush()
            self.db.update_value(self._pos, 1)
            #self._pulse_width_on = 0.01
            #self._pulse_width_off = 0.01
            time.sleep(10)

# --------------------------------------------------

if __name__ == "__main__":
    led_sw = LED_SW(APP_Config.PIN_LED[0], 0, APP_Config.LED_FREQ)


    # Begin calculation


    #led_sw.test()
    #led_sw.led_pwm()

# --------------------------------------------------
