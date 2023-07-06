# --------------------------------------------------

"""App that controls all the HC-SR04 ultrasonic sensors"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import time
import sys
import threading
import multiprocessing as mp
import queue
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
queue_global = queue.Queue()

# All ultrasonic sensors control
class Ultrasonic:
    """Ultrasonic sensors functions"""
    
# --------------------------------------------------
    
    def __init__(self):
        """Ultrasonic initialization"""

        # Variables Initialization
        self._sensor_number = 19
        self._pin_in_use = 0
        self._distance = 0
        self._start_time = 0.0
        #self._time_sleep = 0.05 / self._sensor_number
        #self._time_sleep = 0.003125
        self._time_sleep = 0.003
        #self._time_sleep = 0.05
        self._previous = [0] * 19
        self._sensor_selected = 0
        self._distance_selected = [0] * 19
        self.db_sensor = 0
        self.db_distance = 0
        self.db_ok = 0

        # Database Initialization
        self.db = Database_Sensor()
        self.database_reset()

        # Demultiplexer Intialization
        self.demux = Demux(APP_Config.PIN_D_M_ENABLE, APP_Config.PIN_D_M_ADDRESS)
        self.demux.signal(Demux_Enable[0], Demux_Address[7])

        # Sensor Initialization
        GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
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

        self.hcsr04 = [HCSR04(APP_Config.PIN_SENSOR[0], APP_Config.MAXIMUM_DISTANCE),
                       HCSR04(APP_Config.PIN_SENSOR[1], APP_Config.MAXIMUM_DISTANCE),
                       HCSR04(APP_Config.PIN_SENSOR[2], APP_Config.MAXIMUM_DISTANCE)]

# -------------------------------------------------- 

    def ultrasonic_main_filter_4(self):
        """Main function with filter"""
        # Variables
        values_last = [0]*self._sensor_number
        values_old = [0]*self._sensor_number
        values_old_2 = [0]*self._sensor_number
        values_avg = [0]*self._sensor_number
        values_final = [0]*self._sensor_number

        self.values_distance = values_final

        self.values_sensor = [0]*self._sensor_number
        for value in range(self._sensor_number):
            self.values_sensor[value] = value
            
        # Counters
        counter_enable = 0
        counter_address = 0
        counter_general = 0

        # Database Updater Thread Creation
        self.condition = threading.Condition()
        updater= threading.Thread(target=self.db_update_2, args=())
        updater.start()
        
        #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))
        #sys.stdout.flush()

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        time.sleep(0.1)

        # Loop
        while True:
            for counter_general in range(self._sensor_number):
                if counter_general == 0:
                    time_start_loop = time.monotonic()

                #time_start = time.monotonic()

                # Mux and Demux Address and Enable Selection, Demux Trigger
                self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])
                
                # Distance Measurement
                if counter_general == 2:
                    self._distance = self.hcsr04[counter_enable].measure_ntntnr_long()
                else:
                    self._distance = self.hcsr04[counter_enable].measure_ntntnr()
                
                if self._distance < -5:
                    self._distance = -10
                elif self._distance < 5:
                    self._distance = -100
                elif self._distance > 500 and (counter_general == 2): # Out of Reach
                    self._distance = -1
                elif self._distance > 300: # Out of Reach
                    self._distance = -1

                
                self._distance = round(self._distance, 2)

                # Filter
                # Last 4 values are null and avg > 0-> avg = 0
                if self._distance <= 0 and values_last[counter_general] <= 0 and values_old[counter_general] <= 0 and values_old_2[counter_general] <= 0 and values_avg[counter_general] > 0:
                    values_avg[counter_general] = 0         
                elif self._distance > 0:
                    # Last 4 values > 0 and avg = 0 -> create avg
                    if values_last[counter_general] > 0 and values_old[counter_general] > 0 and values_old_2[counter_general] > 0 and values_avg[counter_general] == 0:
                        values_avg[counter_general] = ( self._distance + values_last[counter_general] + values_old[counter_general] + values_old_2[counter_general] )/4
                    # There is at least 1 not null value and avg > 0 -> update avg
                    elif values_avg[counter_general] > 0:               
                        values_avg[counter_general] = ( self._distance + values_avg[counter_general] )/2

                # Value Update
                value_update = round(values_avg[counter_general],2)
                values_final[counter_general] = value_update

                # Vector Update
                values_old_2[counter_general] = values_old[counter_general]
                values_old[counter_general] = values_last[counter_general]
                values_last[counter_general] = self._distance
                self.db_sensor = counter_general
                self.db_distance = value_update
                self.db_ok = 1
                #_sensor_selected, _distance_selected = self.queue.get()
                #print("1 Saving values:", (_sensor_selected, _distance_selected))
                #sys.stdout.flush()              

                with self.condition:
                    self.condition.notify()

                #print("1 Saving values:", (counter_general, value_update))
                #sys.stdout.flush()

                # Update queue and notify the updater thread
                #print("Putting values in queue:", (counter_general, value_update))
                #sys.stdout.flush()

                # Counter Management
                counter_general = counter_general + 1
                counter_address = counter_address + 1      

                #time_end = time.monotonic()
                #time_short = time_end-time_start
                #print(time_short)
                #sys.stdout.flush()

                if counter_general == 8:
                    counter_enable = 1
                    counter_address = 0
                elif counter_general == 15:
                    counter_enable = 2
                    counter_address = 0
                elif counter_general >= self._sensor_number:
                    counter_address = 0
                    counter_enable = 0
                    counter_general = 0

                    #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  |'.format(*values_last))
                    #sys.stdout.flush()
                    #print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  ||'.format(*values_final))
                    #sys.stdout.flush()

                    #if values_final[14] >= 1:
                    #    print(values_final[14])
                    #    sys.stdout.flush()

                    time_end_loop = time.monotonic()
                    time_loop = time_end_loop-time_start_loop
                    #print(time_loop)
                    #sys.stdout.flush()

                    # Wait
                    if time_loop < 0.06:
                        time.sleep(0.06-time_loop)

                # Wait
                #if counter_general == 2-1 or counter_general == 4-1 or counter_general == 6-1 or counter_general == 17-1:
                #    time.sleep(0.01)
                #else:
                #time.sleep(0.05) #0.0016
                
                #time.sleep(0.1)
                #time.sleep(self._time_sleep)

 # --------------------------------------------------

    def db_update_on(self):
        """Function that udates de database in parallel to the Ultrasonic Main"""

        while True:
            values_sensor = self.values_sensor
            values_distance = self.values_distance
            self.db.update_all(values_sensor, values_distance)

# -------------------------------------------------- 

    def ultrasonic_main(self):
        """Main function"""
        counter_enable = 1
        counter_address = 0
        values = [0]*19
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))

        while True:
            for counter_general in range(len(APP_Config.PIN_SENSOR)):
                # Mux and Demux Address and Enable Selection, Demux Trigger
                self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])
                trigger_time = time.monotonic()

                # Distance Measurement
                self._distance = self.hcsr04[counter_general].measure_ntnr(trigger_time)

                # Database Update
                self.db.update_value(counter_general, round(self._distance, 2))

                # Test Read
                #value_1 = self.db.select_value(counter)
                #print('Sensor {} - {} mm'.format(counter, value_1))
                #sys.stdout.flush()

                values[counter_general] = round(self._distance, 2)

                # Print ALL
                if counter_general == 15:
                    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*values))
                    sys.stdout.flush()

                # Counter Management
                counter_general = counter_general + 1
                counter_address = counter_address + 1
                if counter_general == 8:
                    counter_enable = 1
                    counter_address = 0

                if counter_general >= 1: #len(APP_Config.PIN_SENSOR):
                    counter_general = 0
                    counter_enable = 0
                    counter_address = 0

                # Wait
                time.sleep(self._time_sleep)

# -------------------------------------------------- 

    def test_filter(self):
        """Test Filter"""
        
        GPIO.setup(APP_Config.PIN_SENSOR[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set Sensor pin as INPUT

        sensor_number = 8
        counter_enable = 0
        counter_address = 0

        values_last = [0]*sensor_number
        values_old = [0]*sensor_number
        values_avg = [0]*sensor_number
        values_final = [0]*sensor_number
        print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6}  |'.format(*range(sensor_number)))

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        time.sleep(0.5)

        while True:
            for counter_general in range(sensor_number):

                #if counter_general == 0:
                #    time_start_loop = time.monotonic()

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

                if self._distance < 0: # Error in Voltage
                    self._distance = -100

                if self._distance > 450: # Out of Reach
                    self._distance = -1

                self._distance = round(self._distance, 2)

                # Filter
                # Last 3 values are null and avg > 0-> avg = 0
                if self._distance <= 0 and values_last[counter_general] <= 0 and values_old[counter_general] <= 0 and values_avg[counter_general] > 0:
                    values_avg[counter_general] = 0                
                elif self._distance > 0:
                    # Last 3 values > 0 and avg = 0 -> create avg
                    if values_last[counter_general] > 0 and values_old[counter_general] > 0 and values_avg[counter_general] == 0:
                        values_avg[counter_general] = ( self._distance + values_last[counter_general] + values_old[counter_general] )/3
                    # There is at least 1 not null value and avg > 0 -> update avg
                    if values_avg[counter_general] > 0:               
                        values_avg[counter_general] = ( self._distance + values_avg[counter_general] )/2

                # Value Update
                values_final[counter_general] = round(values_avg[counter_general],2)

                # Vector Update
                values_old[counter_general] = values_last[counter_general]
                values_last[counter_general] = self._distance

                # Database Update
                self.db.update_value(counter_general, round(values_final[counter_general], 2))

                # Counter Management
                counter_general = counter_general + 1
                counter_address = counter_address + 1                

                if counter_general == sensor_number:
                    counter_address = 0
                    counter_general = 0

                    #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6}  |'.format(*values_last))
                    #sys.stdout.flush()
                    print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} ||'.format(*values_final))
                    sys.stdout.flush()

                    #time_end_loop = time.monotonic()
                    #time_loop = time_end_loop-time_start_loop
                    #print(time_loop)
                    #sys.stdout.flush()

                # Wait
                time.sleep(0.1)

# -------------------------------------------------- 

    def ultrasonic_main_filter_3(self):
        """Main function with filter"""
        # Variables
        values_last = [0]*self._sensor_number
        values_old = [0]*self._sensor_number
        values_avg = [0]*self._sensor_number
        values_final = [0]*self._sensor_number
            
        # Counters
        counter_enable = 0
        counter_address = 0
        counter_general = 0
        
        #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))
        #sys.stdout.flush()

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        time.sleep(0.1)

        # Loop
        while True:
            for counter_general in range(self._sensor_number):
                if counter_general == 0:
                    time_start_loop = time.monotonic()

                time_start = time.monotonic()

                # Mux and Demux Address and Enable Selection, Demux Trigger
                self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])

                # Distance Measurement
                if counter_general == 2 or counter_general == 4:
                    self._distance = self.hcsr04[counter_enable].measure_ntntnr_long()
                else:
                    self._distance = self.hcsr04[counter_enable].measure_ntntnr()

                if self._distance < 0:
                    self._distance = -100

                if self._distance > 500: # Out of Reach
                    self._distance = -1

                self._distance = round(self._distance, 2)

                # Filter
                # Last 3 values are null and avg > 0-> avg = 0
                if self._distance <= 0 and values_last[counter_general] <= 0 and values_old[counter_general] <= 0 and values_avg[counter_general] > 0:
                    values_avg[counter_general] = 0                
                elif self._distance > 0:
                    # Last 3 values > 0 and avg = 0 -> create avg
                    if values_last[counter_general] > 0 and values_old[counter_general] > 0 and values_avg[counter_general] == 0:
                        values_avg[counter_general] = ( self._distance + values_last[counter_general] + values_old[counter_general] )/3
                    # There is at least 1 not null value and avg > 0 -> update avg
                    if values_avg[counter_general] > 0:               
                        values_avg[counter_general] = ( self._distance + values_avg[counter_general] )/2

                # Value Update
                values_final[counter_general] = round(values_avg[counter_general],2)

                # Vector Update
                values_old[counter_general] = values_last[counter_general]
                values_last[counter_general] = self._distance

                time_db_start = time.monotonic()

                # Database Update
                self.db.update_value(counter_general, values_final[counter_general])

                time_db_end = time.monotonic()
                time_db = time_db_end-time_db_start
                print(time_db)
                sys.stdout.flush()

                # Counter Management
                counter_general = counter_general + 1
                counter_address = counter_address + 1

                #if counter_general == 2:
                #    print(self._distance)
                #    sys.stdout.flush() 

                time_end = time.monotonic()
                time_short = time_end-time_start
                print(time_short)
                sys.stdout.flush()   

                if counter_general == 8:
                    counter_enable = 1
                    counter_address = 0
                if counter_general == 15:
                    counter_enable = 2
                    counter_address = 0
                if counter_general >= self._sensor_number:
                    counter_address = 0
                    counter_enable = 0
                    counter_general = 0

                    #rint('|   {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}    |'.format(*values_last))
                    #sys.stdout.flush()
                    #print('||  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}   ||'.format(*values_last))
                    #sys.stdout.flush()
                    #print('||| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  |||'.format(*values_final))
                    #sys.stdout.flush()

                    time_end_loop = time.monotonic()
                    time_loop = time_end_loop-time_start_loop
                    print(time_loop)
                    sys.stdout.flush()

                    # Wait
                    if time_loop < 0.06:
                        time.sleep(0.06-time_loop)

                # Wait
                #time.sleep(0.0018)
                time.sleep(0.01)
                #time.sleep(self._time_sleep)

# -------------------------------------------------- 

    def ultrasonic_main_filter_3_new(self):
        """Main function with filter"""
        # Variables
        values_last = [0]*self._sensor_number
        values_old = [0]*self._sensor_number
        values_avg = [0]*self._sensor_number
        values_final = [0]*self._sensor_number
            
        # Counters
        counter_enable = 0
        counter_address = 0
        counter_general = 0

        # Database Updater Thread Creation
        self.queue = queue.Queue()
        self.condition = threading.Condition()
        updater= threading.Thread(target=self.db_update, args=())
        updater.start()
        
        #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))
        #sys.stdout.flush()

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        time.sleep(0.1)

        # Loop
        while True:
            for counter_general in range(self._sensor_number):
                if counter_general == 0:
                    time_start_loop = time.monotonic()

                #time_start = time.monotonic()

                # Mux and Demux Address and Enable Selection, Demux Trigger
                self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])
                
                # Distance Measurement
                if counter_general == 2 or counter_general == 4:
                    self._distance = self.hcsr04[counter_enable].measure_ntntnr_long()
                else:
                    self._distance = self.hcsr04[counter_enable].measure_ntntnr()

                if self._distance < 0:
                    self._distance = -100
                elif self._distance > 500: # Out of Reach
                    self._distance = -1

                self._distance = round(self._distance, 2)

                # Filter
                # Last 3 values are null and avg > 0-> avg = 0
                if self._distance <= 0 and values_last[counter_general] <= 0 and values_old[counter_general] <= 0 and values_avg[counter_general] > 0:
                    values_avg[counter_general] = 0         
                elif self._distance > 0:
                    # Last 3 values > 0 and avg = 0 -> create avg
                    if values_last[counter_general] > 0 and values_old[counter_general] > 0 and values_avg[counter_general] == 0:
                        values_avg[counter_general] = ( self._distance + values_last[counter_general] + values_old[counter_general] )/3
                    # There is at least 1 not null value and avg > 0 -> update avg
                    elif values_avg[counter_general] > 0:               
                        values_avg[counter_general] = ( self._distance + values_avg[counter_general] )/2

                # Value Update
                value_update = round(values_avg[counter_general],2)
                values_final[counter_general] = value_update

                # Vector Update
                values_old[counter_general] = values_last[counter_general]
                values_last[counter_general] = self._distance

                # Update queue and notify the updater thread
                #print("Putting values in queue:", (counter_general, value_update))
                #sys.stdout.flush()
                #queue_global.put((counter_general, value_update))
                self.queue.put((counter_general, value_update))
                #_sensor_selected, _distance_selected = self.queue.get()
                #print("1 Saving values:", (_sensor_selected, _distance_selected))
                #sys.stdout.flush()
                with self.condition:
                    self.condition.notify()

                # Counter Management
                counter_general = counter_general + 2
                counter_address = counter_address + 2      

                #time_end = time.monotonic()
                #time_short = time_end-time_start
                #print(time_short)
                #sys.stdout.flush()  

                if counter_general == 8 or counter_general == 9:
                    counter_enable = 1
                    counter_address = 0
                elif counter_general == 15 or counter_general:
                    counter_enable = 2
                    counter_address = 0
                elif counter_general >= self._sensor_number:
                    counter_address = 0
                    counter_enable = 0
                    counter_general = 0

                    #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  |'.format(*values_last))
                    #sys.stdout.flush()
                    #print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  ||'.format(*values_final))
                    #sys.stdout.flush()

                    time_end_loop = time.monotonic()
                    time_loop = time_end_loop-time_start_loop
                    #print(time_loop)
                    #sys.stdout.flush()

                    # Wait
                    if time_loop < 0.06:
                        time.sleep(0.06-time_loop)

                # Wait
                time.sleep(0.0025)
                #time.sleep(0.1)
                #time.sleep(self._time_sleep)

# -------------------------------------------------- 

    def ultrasonic_main_filter_3_new_2(self):
        """Main function with filter"""
        # Variables
        values_last = [0]*self._sensor_number
        values_old = [0]*self._sensor_number
        values_old_2 = [0]*self._sensor_number
        values_avg = [0]*self._sensor_number
        values_final = [0]*self._sensor_number

        self.values_distance = values_final

        self.values_sensor = [0]*self._sensor_number
        for value in range(self._sensor_number):
            self.values_sensor[value] = value
            
        # Counters
        counter_enable = 0
        counter_address = 0
        counter_general = 0

        # Database Updater Thread Creation
        self.queue = queue.Queue()
        self.condition = threading.Condition()
        updater= threading.Thread(target=self.db_update_2, args=())
        updater.start()
        
        print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))
        sys.stdout.flush()

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        time.sleep(0.1)

        # Loop
        while True:
            for counter_general in range(self._sensor_number):
                if counter_general == 0:
                    time_start_loop = time.monotonic()

                #time_start = time.monotonic()

                # Mux and Demux Address and Enable Selection, Demux Trigger
                self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])
                
                # Distance Measurement
                if counter_general == 2 or counter_general == 4:
                    self._distance = self.hcsr04[counter_enable].measure_ntntnr_long()
                else:
                    self._distance = self.hcsr04[counter_enable].measure_ntntnr()
                if self._distance < -5:
                    self._distance = -10
                elif self._distance < 5:
                    self._distance = -100
                elif self._distance > 300: # Out of Reach
                    self._distance = -1

                self._distance = round(self._distance, 2)

                # Filter
                # Last 3 values are null and avg > 0-> avg = 0
                if self._distance <= 0 and values_last[counter_general] <= 0 and values_old[counter_general] <= 0 and values_avg[counter_general] > 0:
                    values_avg[counter_general] = 0         
                elif self._distance > 0:
                    # Last 3 values > 0 and avg = 0 -> create avg
                    if values_last[counter_general] > 0 and values_old[counter_general] > 0 and values_avg[counter_general] == 0:
                        values_avg[counter_general] = ( self._distance + values_last[counter_general] + values_old[counter_general] )/3
                    # There is at least 1 not null value and avg > 0 -> update avg
                    elif values_avg[counter_general] > 0:               
                        values_avg[counter_general] = ( self._distance + values_avg[counter_general] )/2

                # Value Update
                value_update = round(values_avg[counter_general],2)
                values_final[counter_general] = value_update

                # Vector Update
                values_old[counter_general] = values_last[counter_general]
                values_last[counter_general] = self._distance
                self.db_sensor = counter_general
                self.db_distance = value_update
                self.db_ok = 1
                #_sensor_selected, _distance_selected = self.queue.get()
                #print("1 Saving values:", (_sensor_selected, _distance_selected))
                #sys.stdout.flush()              

                with self.condition:
                    self.condition.notify()

                #print("1 Saving values:", (counter_general, value_update))
                #sys.stdout.flush()

                # Update queue and notify the updater thread
                #print("Putting values in queue:", (counter_general, value_update))
                #sys.stdout.flush()

                # Counter Management
                counter_general = counter_general + 1
                counter_address = counter_address + 1      

                #time_end = time.monotonic()
                #time_short = time_end-time_start
                #print(time_short)
                #sys.stdout.flush()



                if counter_general == 8:
                    counter_enable = 1
                    counter_address = 0
                elif counter_general == 15:
                    counter_enable = 2
                    counter_address = 0
                elif counter_general >= self._sensor_number:
                    counter_address = 0
                    counter_enable = 0
                    counter_general = 0

                    #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  |'.format(*values_last))
                    #sys.stdout.flush()
                    print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  ||'.format(*values_final))
                    sys.stdout.flush()

                    #if values_final[14] >= 1:
                    #    print(values_final[14])
                    #    sys.stdout.flush()

                    time_end_loop = time.monotonic()
                    time_loop = time_end_loop-time_start_loop
                    #print(time_loop)
                    #sys.stdout.flush()

                    # Wait
                    if time_loop < 0.06:
                        time.sleep(0.06-time_loop)

                # Wait
                #if counter_general == 2-1 or counter_general == 4-1 or counter_general == 6-1 or counter_general == 17-1:
                #    time.sleep(0.01)
                #else:
                #time.sleep(0.05) #0.0016
                
                #time.sleep(0.1)
                #time.sleep(self._time_sleep)

# -------------------------------------------------- 

    def ultrasonic_main_loop_filter_3(self):
        """Main function with filter"""

        # Variables
        values_last = [0]*self._sensor_number
        values_old = [0]*self._sensor_number
        values_avg = [0]*self._sensor_number
        values_final = [0]*self._sensor_number
        
        self.values_distance = values_final

        self.values_sensor = [0]*self._sensor_number
        for value in range(self._sensor_number):
            self.values_sensor[value] = value

        # Counters
        counter_general = 0
        counter_enable = 0
        counter_address = 0
        count = 0
        increment = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 1, 3, 5, 7, 9, 11, 13, 15, 17]

        # Database Updater Thread Creation
        self.queue = queue.Queue()
        self.condition = threading.Condition()
        updater= threading.Thread(target=self.db_update_on, args=())
        updater.start()
        
        #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))
        #sys.stdout.flush()

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        time.sleep(0.1)

        while True:
            counter_general = increment[count % len(increment)]
            
            if counter_general <= 7:
                counter_enable = 0
                counter_address = counter_general % 8
            elif counter_general <= 14:
                counter_enable = 1
                counter_address = (counter_general - 8) % 7
            else:
                counter_enable = 2
                counter_address = (counter_general - 15) % 4

            if counter_general == 0:
                time_start_loop = time.monotonic()

            #time_start = time.monotonic()

            # Mux and Demux Address and Enable Selection, Demux Trigger
            self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])
            
            # Distance Measurement
            if counter_general == 2 or counter_general == 4:
                self._distance = self.hcsr04[counter_enable].measure_ntntnr_long()
            else:
                self._distance = self.hcsr04[counter_enable].measure_ntntnr()

            if self._distance < 0:
                self._distance = -100
            elif self._distance > 500: # Out of Reach
                self._distance = -1

            self._distance = round(self._distance, 2)

            # Filter
            # Last 3 values are null and avg > 0-> avg = 0
            if self._distance <= 0 and values_last[counter_general] <= 0 and values_old[counter_general] <= 0 and values_avg[counter_general] > 0:
                values_avg[counter_general] = 0         
            elif self._distance > 0:
                # Last 3 values > 0 and avg = 0 -> create avg
                if values_last[counter_general] > 0 and values_old[counter_general] > 0 and values_avg[counter_general] == 0:
                    values_avg[counter_general] = ( self._distance + values_last[counter_general] + values_old[counter_general] )/3
                # There is at least 1 not null value and avg > 0 -> update avg
                elif values_avg[counter_general] > 0:               
                    values_avg[counter_general] = ( self._distance + values_avg[counter_general] )/2

            # Value Update
            value_update = round(values_avg[counter_general],2)
            values_final[counter_general] = value_update

            # Vector Update
            values_old[counter_general] = values_last[counter_general]
            values_last[counter_general] = self._distance
            self.db_sensor = counter_general
            self.db_distance = value_update
            self.db_ok = 1              

            #time_end = time.monotonic()
            #time_short = time_end-time_start
            #print(time_short)
            #sys.stdout.flush()  

            count += 1
            if count == len(increment):
                count = 0

                #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  |'.format(*values_last))
                #sys.stdout.flush()
                #print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  ||'.format(*values_final))
                #sys.stdout.flush()

                time_end_loop = time.monotonic()
                time_loop = time_end_loop-time_start_loop
                #print(time_loop)
                #sys.stdout.flush()

                # Wait
                if time_loop < 0.06:
                    time.sleep(0.06-time_loop)

# -------------------------------------------------- 

    def ultrasonic_main_filter_2(self):
        """Main function with filter"""
        # Variables
        values_last = [0]*self._sensor_number
        values_avg = [0]*self._sensor_number
        values_final = [0]*self._sensor_number
        
        self.values_sensor = [0]*self._sensor_number
        for value in range(self._sensor_number):
            self.values_sensor[value] = value

        # Counters
        counter_enable = 0
        counter_address = 0
        counter_general = 0
        
        print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))
        sys.stdout.flush()

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        delay_time = 1
        time.sleep(delay_time)

        # Loop
        while True:
            for counter_general in range(self._sensor_number):
                #if counter_general == 0:
                #    time_start_loop = time.monotonic()

                #time_start = time.monotonic()

                # Mux and Demux Address and Enable Selection, Demux Trigger
                self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])

                # Distance Measurement
                self._distance = self.hcsr04[counter_enable].measure_ntntnr()

                if self._distance < 0:
                    self._distance = -100

                if self._distance > 500: # Out of Reach
                    self._distance = -1

                self._distance = round(self._distance, 2)

                # Filter
                # Last 2 values are null and avg > 0-> avg = 0
                if self._distance <= 0 and values_last[counter_general] <= 0 and values_avg[counter_general] > 0:
                    values_avg[counter_general] = 0                
                elif self._distance > 0:
                    # Last 2 values > 0 and avg = 0 -> create avg
                    if values_last[counter_general] > 0 and values_avg[counter_general] == 0:
                        values_avg[counter_general] = ( self._distance + values_last[counter_general] )/2
                    # There is at least 1 not null value and avg > 0 -> update avg
                    if values_avg[counter_general] > 0:               
                        values_avg[counter_general] = ( self._distance + values_avg[counter_general] )/2

                # Value Update
                values_final[counter_general] = round(values_avg[counter_general],2)
                self.values_distance = values_final

                # Vector Update
                values_last[counter_general] = self._distance
                
                self.db.update_value(counter_general, values_final[counter_general])
                # Counter Management
                counter_general = counter_general + 1
                counter_address = counter_address + 1   

                #time_end = time.monotonic()
                #time_short = time_end-time_start
                #print(time_short)             
                if counter_general == 8:
                    counter_enable = 1
                    counter_address = 0
                if counter_general == 15:
                    counter_enable = 2
                    counter_address = 0
                if counter_general == self._sensor_number:
                    counter_address = 0
                    counter_enable = 0
                    counter_general = 0
                    
                    #Database Update
                    #self.db.update_all(values_sensor, values_final)

                    print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  |'.format(*values_last))
                    sys.stdout.flush()
                    print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  ||'.format(*values_final))
                    sys.stdout.flush()

                    #time_end_loop = time.monotonic()
                    #time_loop = time_end_loop-time_start_loop
                    #print(time_loop)
                    #sys.stdout.flush()

                # Wait
                #time.sleep(0.5)
                time.sleep(self._time_sleep)

# -------------------------------------------------- 

    def ultrasonic_main_filter_2_new(self):
        """Main function with filter"""
        # Variables
        sensor_number = 8
        values_sensor = [0]*self._sensor_number
        for value in range(self._sensor_number):
            values_sensor[value] = value
        values_last = [0]*self._sensor_number
        values_avg = [0]*self._sensor_number
        values_final = [0]*self._sensor_number

        # Counters
        counter_enable = 0
        counter_address = 0
        counter_general = 0

        # Database Updater Thread Creation
        #self.queue = queue.Queue()
        self.condition = threading.Condition()
        updater= threading.Thread(target=self.db_update, args=())
        updater.start()
        
        print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))
        sys.stdout.flush()

        self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address+1])
        delay_time = 1
        time.sleep(delay_time)

        # Loop
        while True:
            for counter_general in range(self._sensor_number):
                #if counter_general == 0:
                #    time_start_loop = time.monotonic()

                #time_start = time.monotonic()

                # Variable update
                self._sensor_selected = counter_general

                # Mux and Demux Address and Enable Selection, Demux Trigger
                self.demux.signal(Demux_Enable[counter_enable], Demux_Address[counter_address])

                # Distance Measurement
                self._distance = self.hcsr04[counter_enable].measure_ntntnr()

                if self._distance < 0:
                    self._distance = -100

                if self._distance > 500: # Out of Reach
                    self._distance = -1

                self._distance = round(self._distance, 2)

                # Filter
                # Last 2 values are null and avg > 0-> avg = 0
                if self._distance <= 0 and values_last[counter_general] <= 0 and values_avg[counter_general] > 0:
                    values_avg[counter_general] = 0                
                elif self._distance > 0:
                    # Last 2 values > 0 and avg = 0 -> create avg
                    if values_last[counter_general] > 0 and values_avg[counter_general] == 0:
                        values_avg[counter_general] = ( self._distance + values_last[counter_general] )/2
                    # There is at least 1 not null value and avg > 0 -> update avg
                    if values_avg[counter_general] > 0:               
                        values_avg[counter_general] = ( self._distance + values_avg[counter_general] )/2

                # Value Update
                value_update = round(values_avg[counter_general],2)
                values_final[counter_general] = value_update
                self._distance_selected[counter_general] = value_update

                # Vector Update
                values_last[counter_general] = self._distance

                # Update queue and notify the updater thread
                #print("Putting values in queue:", (counter_general, value_update))
                #sys.stdout.flush()
                queue_global.put((counter_general, value_update))
                #_sensor_selected, _distance_selected = self.queue.get()
                #print("Saving values:", (_sensor_selected, _distance_selected))
                with self.condition:
                    self.condition.notify()

                # Counter Management
                counter_general = counter_general + 1
                counter_address = counter_address + 1

                #time_end = time.monotonic()
                #time_final = time_end-time_start
                #print(time_final)             

                if counter_general == sensor_number:
                    counter_address = 0
                    counter_enable = 0
                    counter_general = 0

                    #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6}  |'.format(*values_last))
                    #sys.stdout.flush()
                    print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} ||'.format(*values_final))
                    sys.stdout.flush()

                    #time_end_loop = time.monotonic()
                    #time_loop = time_end_loop-time_start_loop
                    #print(time_loop)
                    #sys.stdout.flush()

                # Wait
                #time.sleep(0.1)
                time.sleep(self._time_sleep)

# --------------------------------------------------

    def db_update(self):
        """Function that udates de database in parallel to the Ultrasonic Main"""

        #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  |'.format(*range(19)))
        #sys.stdout.flush()
        #vector = [0]*19
        sys.stdout.flush()
        while True:
            with self.condition:
                self.condition.wait()

            while not self.queue.empty():
                _sensor_selected, _distance_selected = self.queue.get()
                #print("2 Saving values:", (_sensor_selected, _distance_selected))
                #sys.stdout.flush()
                self.db.update_value(_sensor_selected, _distance_selected)
                #time.sleep(0.003)
                #data_retrieved = self.db.select_all()
                #for sensor, distance in data_retrieved:
                #    vector[sensor] = distance
                #    if sensor == 18:
                #        print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} ||'.format(*vector))
                #        sys.stdout.flush()

# --------------------------------------------------

    def db_update_2(self):
        """Function that udates de database in parallel to the Ultrasonic Main"""

        #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6}  |'.format(*range(19)))
        #sys.stdout.flush()
        #vector = [0]*19
        #sys.stdout.flush()
        #_sensor_selected = 0
        #vector = [0]*19
        while True:
            #with self.condition:
            #    self.condition.wait()
            #if self.db_ok == 1:
                #self.db_ok = 0
                #_sensor_selected = self.db_sensor 
                #_distance_selected = self.db_distance
                values_sensor = self.values_sensor
                values_distance = self.values_distance
                self.db.update_all(values_sensor, values_distance)
                #self.db.update_value(_sensor_selected, _distance_selected)
                
                #data_retrieved = self.db.select_all()

                #for sensor, distance in data_retrieved:
                #    vector[sensor] = distance
                #    if sensor == 18:
                #        print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*vector))
                #        sys.stdout.flush()

                #print("2 Saving values:", (_sensor_selected, _distance_selected))
                #sys.stdout.flush()
            
            #time.sleep(0.003)
            #data_retrieved = self.db.select_all()
            #for sensor, distance in data_retrieved:
            #    vector[sensor] = distance
            #    if sensor == 18:
            #        print('|| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} ||'.format(*vector))
            #        sys.stdout.flush()

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
    GPIO.setmode(GPIO.BCM) # Use Broadcom (BCM) pin numbering for the GPIO pins
    #sys.stdout.flush()
    ultra = Ultrasonic()

    ultra.ultrasonic_main_filter_4()
    #ultra.ultrasonic_main()
    #ultra.ultrasonic_main_filter_3()
    #ultra.ultrasonic_main_filter_3_new_2()
    #ultra.ultrasonic_main_loop_filter_3()
    #ultra.ultrasonic_main_filter_2()
    #ultra.test()
    #ultra.test_filter()