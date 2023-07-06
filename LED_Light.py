# --------------------------------------------------

"""App that controls all the LEDs"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import time
import threading
import sys
import os

import APP_Config
from LED_PWM_SW import LED_SW
from UI_Pot import Potentiometer
from Drivers.DRV_Switch import Switch
from Drivers.DRV_KY038 import KY038
from Drivers.DRV_Data_LED import Database_LED

# --------------------------------------------------

# Global Variables

COLOURS = [[0, 100, 100], # Cyan
           [0, 50, 100], # Light Blue
           [0, 0, 100], # Blue
           [50, 0, 100], # Violet
           [100, 0, 100], # Magenta
           [100, 0, 75], # Coral
           [100, 0, 0], # Red
           [100, 50, 0], # Orange
           [100, 100, 0], # Yellow
           [50, 100, 0], # Light Green
           [0, 100, 0]] # Green

# --------------------------------------------------
class Light:
    """Functions to control all LEDs"""

# --------------------------------------------------

    def __init__(self):
        """Light initialization"""

        # Variable Initialization
        self.clap_detection = True
        self.clap_counter = 10
        self.pot_stop = 0
        self.clap_counted = 0
        self.clap_cb = 0

        # Clap Switch Setup
        self.switch_2 = Switch(APP_Config.PIN_SWITCH[2], True, self.switch_2_change_cb)
        self.sw_2_status = self.switch_2.read_pin()
        self.clap_stop = self.sw_2_status

        # Database Initialization
        #self.db_mic = Database_Mic()
        self.db_led = Database_LED()
        self.database_reset()

# --------------------------------------------------

    def light_main(self):
        """Main function"""
        
        time.sleep(5)

        # PWM Initialization
        self.led_sw_red = LED_SW(APP_Config.PIN_LED[0], 0, APP_Config.LED_FREQ)
        self.led_sw_green = LED_SW(APP_Config.PIN_LED[1], 1, APP_Config.LED_FREQ)
        self.led_sw_blue = LED_SW(APP_Config.PIN_LED[2], 2, APP_Config.LED_FREQ)
        time.sleep(9)

        self.startup_light_show()
        print('Start Light')
        sys.stdout.flush()

        # Potentiometers Initialization
        self.pot = Potentiometer(self.light_new_duty_cb)
        pot_thread = threading.Thread(target=self.pot.ui_pot_main, args=())
        pot_thread.start()

        # Clap Detection Initialization
        self.mic = KY038(APP_Config.PIN_KY038_DIG, False, True, True, self.light_clap_cb)
        
        while True:
            time.sleep(0.1) # Ajustar
            #self.clap_detected, self.clap_time = self.mic.clap()
            #print(self.clap_detected)
            #print(self.clap_time)
            #print(self.clap_cb)
            #sys.stdout.flush()
            self.sw_2_status = self.switch_2.read_pin()
            self.clap_stop = self.sw_2_status

            # Clap Handling           
            if self.clap_cb == 1:
                self.clap_cb = 0
                #print('waiting for clap')
                #sys.stdout.flush()
                time.sleep(2)
                if self.clap_cb == 1:
                    self.clap_counted = 2
                    #self.clap_cb = 0
                    #print('clapx2')
                    sys.stdout.flush()
                else:
                    self.clap_counted = 1
                    self.clap_cb = 0
                    #print('clapx1')
                    #sys.stdout.flush()

            if self.clap_counted == 2:
                current = COLOURS[self.clap_counter]
                if self.clap_counter+3 >= 11:
                    next = 0
                else:
                    next = COLOURS[self.clap_counter+1]
                self.slow_change(current, next)
                self.clap_counter += 1
                #print('Clap x2')
                #sys.stdout.flush()
                if self.clap_counter >= 11:
                    self.clap_counter = 0
                self.clap_counted = 0

            elif self.clap_counted == 1:
                self.led_sw_red.pwm_calc(COLOURS[self.clap_counter][0])
                self.led_sw_green.pwm_calc(COLOURS[self.clap_counter][1])
                self.led_sw_blue.pwm_calc(COLOURS[self.clap_counter][2])
                self.clap_counter += 1
                #print('Clap x1')
                #sys.stdout.flush()
                if self.clap_counter >= 11:
                    self.clap_counter = 0
                self.clap_counted = 0

# --------------------------------------------------

    def startup_light_show(self):
        """Startup light routine"""

        for i in range(11):
            self.led_sw_red.pwm_calc(COLOURS[i][0])
            self.led_sw_green.pwm_calc(COLOURS[i][1])
            self.led_sw_blue.pwm_calc(COLOURS[i][2])
            time.sleep(0.5) # Ajustar

# --------------------------------------------------

    def slow_change(self, current, next):
        """Function that slowly switches from a colour to another"""

        steps = 15  # number of steps in the slow change
        for i in range(steps):
            r = int(current[0] - (current[0] - next[0]) / (steps-1) * i)  # calculate current red value
            g = int(current[1] - (current[1] - next[1]) / (steps-1) * i)  # calculate current green value
            b = int(current[2] - (current[2] - next[2]) / (steps-1) * i)  # calculate current blue value
            self.led_sw_red.pwm_calc(r)
            self.led_sw_green.pwm_calc(g)
            self.led_sw_blue.pwm_calc(b)            
            time.sleep(0.2)  # wait for 0.1 second before next step

# --------------------------------------------------

    def database_reset(self):
        """Function that resets the values in the sensor database"""

        #self.db_mic.update_value(0, 0)
        self.db_led.update_value(0, 0)
        self.db_led.update_value(1, 0)
        self.db_led.update_value(2, 0)
        self.db_led.update_value(3, 0)

# --------------------------------------------------

    def light_clap_cb(self, *args):
        """Callback that comes up when there is a clap detected"""

        if self.clap_detection is True and self.clap_stop == 0:
            #self.led_sw_red.pwm_calc(COLOURS[self.clap_counter][0])
            #self.led_sw_green.pwm_calc(COLOURS[self.clap_counter][1])
            #self.led_sw_blue.pwm_calc(COLOURS[self.clap_counter][2])
            #self.clap_counter += 1
            #print('Clap cb')
            #sys.stdout.flush()
            #if self.clap_counter >= 11:
            #    self.clap_counter = 0
            #self.update_variable()
            self.clap_cb = 1

# --------------------------------------------------

    def switch_2_change_cb(self, *args):
        """Callback that comes up when a change in the status of the switch 2 is detected"""

        #print('switch cb')
        #sys.stdout.flush()
        if self.clap_stop == 0:
            self.clap_stop = 1
        else:
            self.clap_stop = 0

# --------------------------------------------------

    def light_new_duty_cb(self, pos, new_duty):
        """Callback that comes up when there is a change in the potentiometers"""

        self.db_led.update_value(pos, new_duty)
        white = self.db_led.select_value(3)
        percent_white = white/100
        if self.pot_stop == 0:
            if pos == 0:
                self.led_sw_red.pwm_calc(new_duty*percent_white)
                #print('red_cb')
                #sys.stdout.flush()
            elif pos == 1:
                self.led_sw_green.pwm_calc(new_duty*percent_white)
                #print('green_cb')
                #sys.stdout.flush()
            elif pos == 2:
                self.led_sw_blue.pwm_calc(new_duty*percent_white)
                #print('blue_cb')
                #sys.stdout.flush()
            elif pos == 3:
                red_duty = self.db_led.select_value(0)
                green_duty = self.db_led.select_value(1)
                blue_duty = self.db_led.select_value(2)
                self.led_sw_red.pwm_calc(red_duty*percent_white)
                self.led_sw_green.pwm_calc(green_duty*percent_white)
                self.led_sw_blue.pwm_calc(blue_duty*percent_white)
                #print('white_cb')
                #sys.stdout.flush()

# --------------------------------------------------

if __name__ == "__main__":
    light = Light()
    light.light_main()
    # def cb(self):
    #    print("clap")
    #    sys.stdout.flush()
    #callback = partial(light.light_main)
    #ky038 = KY038(APP_Config.PIN_KY038_DIG, 0, True, True, light.light_main)
    while True:
        time.sleep(10)

# --------------------------------------------------
