# --------------------------------------------------

"""App that controls Music Reproduction"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

from ast import Pass
import time
import sys
from Drivers.DRV_Data_Sensor import Database_Sensor
from Drivers.DRV_Sound_MIDI import Sound_MIDI
from Drivers.DRV_Sound_WAV import Sound_WAV
from Drivers.DRV_Sound_Tone import Sound_Tone
from Drivers.DRV_Sound_Tone_Full import Sound_Tone_Full
from Drivers.DRV_Switch import Switch
import Drivers.Values_MIDI as DATA_MIDI
import Drivers.Values_Tone as DATA_Tone
import APP_Config

import multiprocessing as mp
from Ultrasonic import Ultrasonic

# --------------------------------------------------

class Music:
    """Music Reproduction Functions"""

# --------------------------------------------------

    def __init__(self):
        """Music initialization"""
        # Variable Initialization
        self.playing = [0]*19
        self.min_dist = 50
        self.max_dist = 297
        #self.distance_vector = [10, 100, 150, 200, 250, 300, 350, 400]
        #self.distance_vector = [10, 60, 70, 120, 130, 180, 190, 240, 250, 300, 310, 360, 370, 420, 430, 480, 490, 540, 550, 600]
        self.distance_vector = [10, 40, 60, 90, 110, 140, 160, 190, 210, 240, 260, 290, 310, 340, 360, 390, 410, 440, 460, 490]
        self.instrument = [0, 8, 14, 24, 35, 46, 98, 106, 114, 115, 116, 117, 119, 122, 123]
        self.mute_sector = [0]*4

        # Mode Variables
        self.Mode_1_notes = [DATA_MIDI.C,  DATA_MIDI.D,  DATA_MIDI.E,  DATA_MIDI.F,  DATA_MIDI.G,  DATA_MIDI.A,  DATA_MIDI.B,
                             DATA_MIDI.C0, DATA_MIDI.D0, DATA_MIDI.E0, DATA_MIDI.F0, DATA_MIDI.G0, DATA_MIDI.A0, DATA_MIDI.B0,
                             DATA_MIDI.C1, DATA_MIDI.D1, DATA_MIDI.E1, DATA_MIDI.F1, DATA_MIDI.G1, DATA_MIDI.A1, DATA_MIDI.B1,
                             DATA_MIDI.C2, DATA_MIDI.D2, DATA_MIDI.E2, DATA_MIDI.F2, DATA_MIDI.G2, DATA_MIDI.A2, DATA_MIDI.B2,
                             DATA_MIDI.C3, DATA_MIDI.D3, DATA_MIDI.E3, DATA_MIDI.F3, DATA_MIDI.G3, DATA_MIDI.A3, DATA_MIDI.B3,
                             DATA_MIDI.C4, DATA_MIDI.D4, DATA_MIDI.E4, DATA_MIDI.F4, DATA_MIDI.G4, DATA_MIDI.A4, DATA_MIDI.B4,
                             DATA_MIDI.C5, DATA_MIDI.D5, DATA_MIDI.E5, DATA_MIDI.F5, DATA_MIDI.G5, DATA_MIDI.A5, DATA_MIDI.B5,
                             DATA_MIDI.C6, DATA_MIDI.D6, DATA_MIDI.E6, DATA_MIDI.F6, DATA_MIDI.G6, DATA_MIDI.A6, DATA_MIDI.B6,
                             DATA_MIDI.C7, DATA_MIDI.D7, DATA_MIDI.E7, DATA_MIDI.F7, DATA_MIDI.G7, DATA_MIDI.A7, DATA_MIDI.B7,]
        self.Mode_4_notes = [DATA_MIDI.C,  DATA_MIDI.D,  DATA_MIDI.E,  DATA_MIDI.G,  DATA_MIDI.A,
                             DATA_MIDI.C0, DATA_MIDI.D0, DATA_MIDI.E0, DATA_MIDI.G0, DATA_MIDI.A0,
                             DATA_MIDI.C1, DATA_MIDI.D1, DATA_MIDI.E1, DATA_MIDI.G1, DATA_MIDI.A1,
                             DATA_MIDI.C2, DATA_MIDI.D2, DATA_MIDI.E2, DATA_MIDI.G2, DATA_MIDI.A2,
                             DATA_MIDI.C3, DATA_MIDI.D3, DATA_MIDI.E3, DATA_MIDI.G3, DATA_MIDI.A3,
                             DATA_MIDI.C4, DATA_MIDI.D4, DATA_MIDI.E4, DATA_MIDI.G4, DATA_MIDI.A4,
                             DATA_MIDI.C5, DATA_MIDI.D5, DATA_MIDI.E5, DATA_MIDI.G5, DATA_MIDI.A5,
                             DATA_MIDI.C6, DATA_MIDI.D6, DATA_MIDI.E6, DATA_MIDI.G6, DATA_MIDI.A6,
                             DATA_MIDI.C7, DATA_MIDI.D7, DATA_MIDI.E7, DATA_MIDI.G7, DATA_MIDI.A7,
                             DATA_MIDI.C8, DATA_MIDI.D8, DATA_MIDI.E8, DATA_MIDI.G8, DATA_MIDI.A8,]
        self.Mode_5_notes = [DATA_MIDI.C,  DATA_MIDI.C_S,  DATA_MIDI.D,  DATA_MIDI.D_S,  DATA_MIDI.E,  DATA_MIDI.F,  DATA_MIDI.F_S,  DATA_MIDI.G,  DATA_MIDI.G_S,  DATA_MIDI.A,  DATA_MIDI.A_S,  DATA_MIDI.B,
                             DATA_MIDI.C0, DATA_MIDI.C0_S, DATA_MIDI.D0, DATA_MIDI.D0_S, DATA_MIDI.E0, DATA_MIDI.F0, DATA_MIDI.F0_S, DATA_MIDI.G0, DATA_MIDI.G0_S, DATA_MIDI.A0, DATA_MIDI.A0_S, DATA_MIDI.B0,
                             DATA_MIDI.C1, DATA_MIDI.C1_S, DATA_MIDI.D1, DATA_MIDI.D1_S, DATA_MIDI.E1, DATA_MIDI.F1, DATA_MIDI.F1_S, DATA_MIDI.G1, DATA_MIDI.G1_S, DATA_MIDI.A1, DATA_MIDI.A1_S, DATA_MIDI.B1,
                             DATA_MIDI.C2, DATA_MIDI.C2_S, DATA_MIDI.D2, DATA_MIDI.D2_S, DATA_MIDI.E2, DATA_MIDI.F2, DATA_MIDI.F2_S, DATA_MIDI.G2, DATA_MIDI.G2_S, DATA_MIDI.A2, DATA_MIDI.A2_S, DATA_MIDI.B2,
                             DATA_MIDI.C3, DATA_MIDI.C3_S, DATA_MIDI.D3, DATA_MIDI.D3_S, DATA_MIDI.E3, DATA_MIDI.F3, DATA_MIDI.F3_S, DATA_MIDI.G3, DATA_MIDI.G3_S, DATA_MIDI.A3, DATA_MIDI.A3_S, DATA_MIDI.B3,
                             DATA_MIDI.C4, DATA_MIDI.C4_S, DATA_MIDI.D4, DATA_MIDI.D4_S, DATA_MIDI.E4, DATA_MIDI.F4, DATA_MIDI.F4_S, DATA_MIDI.G4, DATA_MIDI.G4_S, DATA_MIDI.A4, DATA_MIDI.A4_S, DATA_MIDI.B4,
                             DATA_MIDI.C5, DATA_MIDI.C5_S, DATA_MIDI.D5, DATA_MIDI.D5_S, DATA_MIDI.E5, DATA_MIDI.F5, DATA_MIDI.F5_S, DATA_MIDI.G5, DATA_MIDI.G5_S, DATA_MIDI.A5, DATA_MIDI.A5_S, DATA_MIDI.B5,
                             DATA_MIDI.C6, DATA_MIDI.C6_S, DATA_MIDI.D6, DATA_MIDI.D6_S, DATA_MIDI.E6, DATA_MIDI.F6, DATA_MIDI.F6_S, DATA_MIDI.G6, DATA_MIDI.G6_S, DATA_MIDI.A6, DATA_MIDI.A6_S, DATA_MIDI.B6,
                             DATA_MIDI.C7, DATA_MIDI.C7_S, DATA_MIDI.D7, DATA_MIDI.D7_S, DATA_MIDI.E7, DATA_MIDI.F7, DATA_MIDI.F7_S, DATA_MIDI.G7, DATA_MIDI.G7_S, DATA_MIDI.A7, DATA_MIDI.A7_S, DATA_MIDI.B7,]
        self.Mode_6_notes = [DATA_MIDI.C,  DATA_MIDI.C_S,  DATA_MIDI.D,  DATA_MIDI.D_S,  DATA_MIDI.E,  DATA_MIDI.F,  DATA_MIDI.F_S,  DATA_MIDI.G,  DATA_MIDI.G_S,  DATA_MIDI.A,  DATA_MIDI.A_S,  DATA_MIDI.B,
                             DATA_MIDI.C0, DATA_MIDI.C0_S, DATA_MIDI.D0, DATA_MIDI.D0_S, DATA_MIDI.E0, DATA_MIDI.F0, DATA_MIDI.F0_S, DATA_MIDI.G0, DATA_MIDI.G0_S, DATA_MIDI.A0, DATA_MIDI.A0_S, DATA_MIDI.B0,
                             DATA_MIDI.C1, DATA_MIDI.C1_S, DATA_MIDI.D1, DATA_MIDI.D1_S, DATA_MIDI.E1, DATA_MIDI.F1, DATA_MIDI.F1_S, DATA_MIDI.G1, DATA_MIDI.G1_S, DATA_MIDI.A1, DATA_MIDI.A1_S, DATA_MIDI.B1,
                             DATA_MIDI.C2, DATA_MIDI.C2_S, DATA_MIDI.D2, DATA_MIDI.D2_S, DATA_MIDI.E2, DATA_MIDI.F2, DATA_MIDI.F2_S, DATA_MIDI.G2, DATA_MIDI.G2_S, DATA_MIDI.A2, DATA_MIDI.A2_S, DATA_MIDI.B2,
                             DATA_MIDI.C3, DATA_MIDI.C3_S, DATA_MIDI.D3, DATA_MIDI.D3_S, DATA_MIDI.E3, DATA_MIDI.F3, DATA_MIDI.F3_S, DATA_MIDI.G3, DATA_MIDI.G3_S, DATA_MIDI.A3, DATA_MIDI.A3_S, DATA_MIDI.B3,
                             DATA_MIDI.C4, DATA_MIDI.C4_S, DATA_MIDI.D4, DATA_MIDI.D4_S, DATA_MIDI.E4, DATA_MIDI.F4, DATA_MIDI.F4_S, DATA_MIDI.G4, DATA_MIDI.G4_S, DATA_MIDI.A4, DATA_MIDI.A4_S, DATA_MIDI.B4,
                             DATA_MIDI.C5, DATA_MIDI.C5_S, DATA_MIDI.D5, DATA_MIDI.D5_S, DATA_MIDI.E5, DATA_MIDI.F5, DATA_MIDI.F5_S, DATA_MIDI.G5, DATA_MIDI.G5_S, DATA_MIDI.A5, DATA_MIDI.A5_S, DATA_MIDI.B5,
                             DATA_MIDI.C6, DATA_MIDI.C6_S, DATA_MIDI.D6, DATA_MIDI.D6_S, DATA_MIDI.E6, DATA_MIDI.F6, DATA_MIDI.F6_S, DATA_MIDI.G6, DATA_MIDI.G6_S, DATA_MIDI.A6, DATA_MIDI.A6_S, DATA_MIDI.B6,
                             DATA_MIDI.C7, DATA_MIDI.C7_S, DATA_MIDI.D7, DATA_MIDI.D7_S, DATA_MIDI.E7, DATA_MIDI.F7, DATA_MIDI.F7_S, DATA_MIDI.G7, DATA_MIDI.G7_S, DATA_MIDI.A7, DATA_MIDI.A7_S, DATA_MIDI.B7,]
        self.mode_2_timer = [0]*19
        self.mode_3_timer = [0]*19 
        self.mode_7_timer = [0]*19
        self.mode_1_octave_select = 0
        self.mode_1_channel_select = 0
        self.mode_4_octave_select = 0
        self.mode_4_channel_select = 0
        self.mode_5_octave_select = 0
        self.mode_5_channel_select = 0
        self.mode_6_octave_select = 0
        self.mode_6_channel_select = 0
        self.start_special = 0
        self.running_special = False
        self.distance_1 = 0
        self.distance_3 = 0

        # Chord and Arpeggios Variables
        self.arpeggio_mi_playing = [0]*19
        self.arpeggio_ma_playing = [0]*19

        # Switch and Mode Selection Variables
        self.sw_0_status = 0
        self.sw_0_status_new = 0
        self.sw_1_status = 0
        self.sw_1_status_new = 0
        self.sw_change = False
        self.current_mode = 0
        self.special_mode = 0

        # Mute Variables
        self.sector1_mute = 0
        self.sector2_mute = 0
        self.sector3_mute = 0
        self.sector4_mute = 0

        # Database Initialization
        self.db = Database_Sensor()

        # Sound Reproduction Initialization
        self.sound_midi = Sound_MIDI()
        time.sleep(0.1)
        self.sound_wav = Sound_WAV()
        time.sleep(0.1)
        self.sound_tone = Sound_Tone()
        time.sleep(0.1)
        self.sound_tone_full = Sound_Tone_Full(DATA_Tone.C4-40, DATA_Tone.C4+440)
        time.sleep(0.1)

        # Switch Initialization
        self.switch_0 = Switch(APP_Config.PIN_SWITCH[0], True, self.switch_0_change_cb)
        self.switch_1 = Switch(APP_Config.PIN_SWITCH[1], True, self.switch_1_change_cb)
        self.sw_0_status_new = self.switch_0.read_pin()
        self.sw_1_status_new = self.switch_1.read_pin()
        self.sw_0_status = self.sw_0_status_new
        self.sw_1_status = self.sw_1_status_new
        self.sw_0_status_old = self.sw_0_status_new
        self.sw_1_status_old = self.sw_1_status_new
        self.sw_0_status_old_2 = self.sw_0_status_old
        self.sw_1_status_old_2 = self.sw_1_status_old
        self.set_mode()

        # Set instruments
        for value in range(15):
            self.sound_midi.set_instrument_and_channel(instrument=self.instrument[value], channel=value)

        # Get WAV lengths
        self.WAV_length = [0]*45
        for value in range(45):
            self.WAV_length[value] = self.sound_wav.get_len(value)

# --------------------------------------------------

    def main_final(self):
        """Main function"""

        # Openning sequence
        time.sleep(0.5)
        self.sound_midi.arpeggio_ma_on(0, self.Mode_5_notes[24], 127)
        time.sleep(1.5)
        self.sound_midi.arpeggio_ma_off(0, self.Mode_5_notes[24])
        self.sound_midi.arpeggio_ma_on(0, self.Mode_5_notes[27], 127)
        time.sleep(1.5)
        self.sound_midi.arpeggio_ma_off(0, self.Mode_5_notes[27])
        self.sound_midi.arpeggio_ma_on(0, self.Mode_5_notes[29], 127)
        time.sleep(1.5)
        self.sound_midi.arpeggio_ma_off(0, self.Mode_5_notes[29])
        self.sound_midi.one_note_on(9, DATA_MIDI.C3, 127)
        time.sleep(1.5)
        self.sound_midi.one_note_off(9, DATA_MIDI.C3)

        # Main Loop
        while True:
            time.sleep(0.01)

            # Switch Status
            self.sw_0_status = self.sw_0_status_new
            self.sw_1_status = self.sw_1_status_new

            print("Special Mode:", self.special_mode)
            sys.stdout.flush()
            print("Current Mode:", self.current_mode)
            sys.stdout.flush()

            # Mode Selection            
            if self.special_mode == 0:
                # Set Normal Modes
                self.set_mode()
                if self.current_mode == 1:
                    print('Mode 1')
                    sys.stdout.flush()
                    self.playing = [0]*19
                    self.mode_1()                    
                elif self.current_mode == 2:
                    print('Mode 2')
                    sys.stdout.flush()
                    self.playing = [0]*19
                    self.mode_2()
                elif self.current_mode == 3:
                    print('Mode 3')
                    sys.stdout.flush()
                    self.playing = [0]*19
                    self.mode_3()
                elif self.current_mode == 4:
                    print('Mode 4')
                    sys.stdout.flush()
                    self.playing = [0]*19
                    self.mode_4()

            if self.special_mode == 1:
                #Set Special Modes
                if self.current_mode == 5:
                    print('Mode 5')
                    sys.stdout.flush()
                    self.sound_midi.arpeggio_ma_on(0, self.Mode_5_notes[27], 127)
                    time.sleep(1)
                    self.sound_midi.arpeggio_ma_off(0, self.Mode_5_notes[27])
                    self.sound_midi.arpeggio_ma_on(0, self.Mode_5_notes[29], 127)
                    time.sleep(1)
                    self.sound_midi.arpeggio_ma_off(0, self.Mode_5_notes[29])
                    self.playing = [0]*19
                    self.mode_5()
                elif self.current_mode == 7:
                    print('Mode 7')
                    sys.stdout.flush()
                    self.sound_midi.arpeggio_ma_on(0, self.Mode_5_notes[27], 127)
                    time.sleep(1)
                    self.sound_midi.arpeggio_ma_off(0, self.Mode_5_notes[27])
                    self.sound_midi.arpeggio_ma_on(0, self.Mode_5_notes[29], 127)
                    time.sleep(1)
                    self.sound_midi.arpeggio_ma_off(0, self.Mode_5_notes[29])
                    self.playing = [0]*19
                    self.mode_7()

# --------------------------------------------------

    def set_mode(self):
        """Mode setting function"""

        if self.sw_0_status == 0 and self.sw_1_status == 0:
            self.current_mode = 1
        elif self.sw_0_status == 0 and self.sw_1_status == 1:
            self.current_mode = 4
        elif self.sw_0_status == 1 and self.sw_1_status == 0:
            self.current_mode = 3
        else:
            self.current_mode = 2
        
        self.sw_change = False
        self.sw_0_status = self.sw_0_status_new
        self.sw_1_status = self.sw_1_status_new

# --------------------------------------------------

    def check_mute(self, sensor, distance):
        """Function that checks if sectors are muted"""

        #if sensor == 15:
        #    if self.mute(distance) == 1:
        #        self.sector1_mute = 1
        #    else:
        #        self.sector1_mute = 0
        #elif sensor == 16:
        #    if self.mute(distance) == 1:
        #        self.sector2_mute = 1
        #    else:
        #        self.sector2_mute = 0
        if sensor == 17:
            if 0 < distance <= 150:
                self.sector3_mute = 1
            else:
                self.sector3_mute = 0
            #print('17 - s3')
            #print(self.sector3_mute)
            #sys.stdout.flush()
        elif sensor == 18:
            if 0 < distance <= 150:
                self.sector4_mute = 1
            else:
                self.sector4_mute = 0
            #print('18 - s4')
            #print(self.sector4_mute)
            #sys.stdout.flush()

# --------------------------------------------------

    def check_special_modes(self, sensor, distance):
        """Function that checks if there should be a change to the special modes"""

        if self.special_mode == 0 and sensor == 1:
            self.distance_1 = distance
        elif self.special_mode == 0 and sensor == 3:
            self.distance_3 = distance
        if self.special_mode == 0 and 0 < self.distance_1 < 100 and 0 < self.distance_3 < 100 and self.running_special == False:
            self.start_special = time.monotonic()
            self.running_special = True
        elif self.special_mode == 0 and (self.distance_1 < 0 or self.distance_1 > 200 or self.distance_3 < 0 or self.distance_3 > 200) and self.running_special == True:
            self.running_special = False
        elif self.special_mode == 0 and 0 < self.distance_1 < 100 and 0 < self.distance_3 < 100 and self.running_special == True and self.start_special+5 <= time.monotonic()+0.01:
            if self.current_mode == 1:
                self.special_mode = 1
                self.current_mode = 5
                print('Select Mode 5')
                sys.stdout.flush()
            elif self.current_mode == 4:
                self.special_mode = 1
                self.current_mode = 7
                print('Select Mode 7')
                sys.stdout.flush()

# --------------------------------------------------

    def check_switches(self):
        """Function that checks the status of both switches"""

        self.sw_0_status_old_2 = self.sw_0_status_old
        self.sw_1_status_old_2 = self.sw_1_status_old
        self.sw_0_status_old = self.sw_0_status_new
        self.sw_1_status_old = self.sw_1_status_new
        self.sw_0_status_new = self.switch_0.read_pin()
        self.sw_1_status_new = self.switch_1.read_pin()
        if (self.sw_0_status_new == self.sw_0_status_old and self.sw_0_status_new == self.sw_0_status_old_2 and self.sw_0_status_new is not self.sw_0_status) or (self.sw_1_status_new == self.sw_1_status_old and self.sw_1_status_new == self.sw_1_status_old_2 and self.sw_1_status_new is not self.sw_1_status):
            self.sw_change = True
            self.special_mode = 0

# --------------------------------------------------

    def mode_1(self):
        """Mode 1 function"""

        print('Start Mode 1')
        sys.stdout.flush()
        #print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*range(19)))
        #sys.stdout.flush()
        #vector = [0]*19

        while self.sw_change is False and self.special_mode == 0:

            data_retrieved = self.db.select_all()

            time.sleep(0.02)

            # Switches Check --------------------------------------------------
            self.check_switches()
            
            # Previous Checks --------------------------------------------------
            for sensor, distance in data_retrieved:        

                # Check special modes --------------------------------------------------
                self.check_special_modes(sensor, distance)
                        
                # Check muted sectors --------------------------------------------------
                if 17 <= sensor <= 18:
                    self.check_mute(sensor, distance)

            # Main Loop --------------------------------------------------
            for sensor, distance in data_retrieved:
                #vector[sensor] = distance
                #if sensor == 18:
                #    print('|  {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} | {16:>6} | {17:>6} | {18:>6} |'.format(*vector))
                #    sys.stdout.flush()

                # Turn On --------------------------------------------------
                if distance > 10 and self.playing[sensor] == 0:

                    # Sensor 0 (Snare)
                    if  distance < 400 and sensor == 0 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(9, DATA_MIDI.C4, 127)
                        self.playing[sensor] = 1                       

                    # Sensor 1 (Major Chord)
                    elif sensor == 1 and self.sector4_mute == 0:
                        for s1_counter in range(5,11+1,1):
                            if self.playing[s1_counter] == 1 and self.arpeggio_mi_playing[s1_counter] == 0:
                                self.sound_midi.arpeggio_mi_on(self.mode_1_channel_select, self.Mode_1_notes[s1_counter-5+7*self.mode_1_octave_select], 127)
                                self.arpeggio_mi_playing[s1_counter] = 1
                        self.playing[sensor] = 1

                    # Sensor 2 (Select Instrument)
                    elif sensor == 2 and self.sector3_mute == 0:
                        for s2_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s2_counter]
                            upper_bound = self.distance_vector[2*s2_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                self.sound_midi.one_note_on(s2_counter, self.Mode_1_notes[12+7*self.mode_1_octave_select], 127)
                                self.mode_1_channel_select = s2_counter
                        self.playing[sensor] = 1

                    # Sensor 3 (Major Arpeggio)
                    elif sensor == 3 and self.sector3_mute == 0:
                        for s3_counter in range(5,11+1,1):
                            if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                                self.sound_midi.arpeggio_ma_on(self.mode_1_channel_select, self.Mode_1_notes[s3_counter-5+7*self.mode_1_octave_select], 127)
                                self.arpeggio_ma_playing[s3_counter] = 1
                        self.playing[sensor] = 1

                    # Sensor 4 (Select Octave)
                    elif sensor == 4 and self.sector3_mute == 0:
                        for s4_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s4_counter]
                            upper_bound = self.distance_vector[2*s4_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                self.sound_midi.one_note_on(self.mode_1_channel_select, self.Mode_1_notes[7*s4_counter], 127)
                                self.mode_1_octave_select = s4_counter
                        self.playing[sensor] = 1
                    
                    # Sensor 5, 6, 7, 8, 9 (Major Scale)
                    elif distance < 400 and sensor >= 5 and sensor <= 9 and self.sector3_mute == 0:
                        self.sound_midi.one_note_on(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1
                        elif self.playing[1] == 1 and self.arpeggio_mi_playing[s1_counter] == 0: # Major Chord
                            self.sound_midi.arpeggio_mi_on(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select], 127)
                            self.arpeggio_mi_playing[sensor] = 1

                    # Sensor 10, 11 (Major Scale)
                    elif distance < 400 and sensor >= 10 and sensor <= 11 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1
                        elif self.playing[1] == 1 and self.arpeggio_mi_playing[s1_counter] == 0: # Major Chord
                            self.sound_midi.arpeggio_mi_on(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select], 127)
                            self.arpeggio_mi_playing[sensor] = 1

                    # Sensor 12 (Drum)
                    elif distance < 400 and sensor == 12 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(10, DATA_MIDI.C, 127)
                        self.playing[sensor] = 1

                    # Sensor 13 (Tom)
                    elif distance < 400 and sensor == 13 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(11, DATA_MIDI.C, 127)
                        self.playing[sensor] = 1

                    # Sensor 14 (Cymbal)
                    elif distance < 400 and sensor == 14 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(12, DATA_MIDI.C3, 127)
                        self.playing[sensor] = 1

                    # Sensor 15 (Snare)
                    elif distance < 400 and sensor == 15 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(10, DATA_MIDI.C4, 127)
                        self.playing[sensor] = 1

                    # Sensor 16 (Tom)
                    elif distance < 400 and sensor == 16 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(11, DATA_MIDI.C, 127)
                        self.playing[sensor] = 1

                # Playing --------------------------------------------------
                elif distance > 10 and self.playing[sensor] == 1 and 1 <= sensor <= 4:

                    # Sensor 1 (Major Chord)
                    if sensor == 1 and self.sector4_mute == 0:
                        for s1_counter in range(5,11+1,1):
                            if self.playing[s1_counter] == 1 and self.arpeggio_mi_playing[s1_counter] == 0:
                                self.sound_midi.arpeggio_mi_on(self.mode_1_channel_select, self.Mode_1_notes[s1_counter-5+7*self.mode_1_octave_select], 127)
                                self.arpeggio_mi_playing[s1_counter] == 1
                        self.playing[sensor] = 1

                    # Sensor 2 (Select Instrument)
                    elif sensor == 2 and self.sector3_mute == 0:
                        for s2_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s2_counter]
                            upper_bound = self.distance_vector[2*s2_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                if s2_counter is not self.mode_1_channel_select:
                                    self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[12+7*self.mode_1_octave_select])
                                    self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[12+7*self.mode_1_octave_select])
                                    self.sound_midi.one_note_on(s2_counter, self.Mode_1_notes[12+7*self.mode_1_octave_select], 127)
                                    self.mode_1_channel_select = s2_counter
                        self.playing[sensor] = 1

                    # Sensor 3 (Major Arpeggio)
                    if sensor == 3 and self.sector3_mute == 0:
                        for s3_counter in range(5,11+1,1):
                            if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                                self.sound_midi.arpeggio_ma_on(self.mode_1_channel_select, self.Mode_1_notes[s3_counter-5+7*self.mode_1_octave_select], 127)
                                self.arpeggio_ma_playing[s3_counter] == 1
                        self.playing[sensor] = 1

                    # Sensor 4 (Select Octave)
                    elif sensor == 4 and distance < 400 and self.sector3_mute == 0:
                        for s4_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s4_counter]
                            upper_bound = self.distance_vector[2*s4_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                if s4_counter is not self.mode_1_octave_select:
                                    self.sound_midi.notes_off(self.mode_1_channel_select, self.Mode_1_notes[7*self.mode_1_octave_select])
                                    self.sound_midi.notes_off(self.mode_1_channel_select, self.Mode_1_notes[7*self.mode_1_octave_select])
                                    self.sound_midi.one_note_on(self.mode_1_channel_select, self.Mode_1_notes[7*s4_counter], 127)
                                    self.mode_1_octave_select = s4_counter
                        self.playing[sensor] = 1

                # Turn Off --------------------------------------------------
                elif (2 <= sensor <= 9 ) and ((distance <= 0 or self.sector3_mute == 1) and self.playing[sensor] == 1):

                    # Sensor 2 (Select Instrument)
                    if sensor == 2:
                        self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[12+7*self.mode_1_octave_select])
                        self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[12+7*self.mode_1_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 3 (Major Arpeggio)
                    elif sensor == 3:
                        for s3_counter in range(5,11+1,1):
                            if self.playing[s3_counter] == 1:
                                self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[s3_counter-5+7*self.mode_1_octave_select])
                                self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[s3_counter-5+7*self.mode_1_octave_select])
                                self.arpeggio_ma_playing[s3_counter] = 0
                        self.playing[sensor] = 0  

                    # Sensor 4 (Select Octave)
                    elif sensor == 4:
                        sys.stdout.flush()
                        self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[7*self.mode_1_octave_select])
                        self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[7*self.mode_1_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 5, 6, 7, 8, 9 (Major Scale)
                    elif  sensor >= 5 and sensor <= 9:
                        if self.playing[1] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                            self.arpeggio_mi_playing[sensor] = 0
                        elif self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                        self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                        self.playing[sensor] = 0 

                elif (10 <= sensor <= 14 or sensor == 15 or sensor == 16 or sensor == 0 or sensor == 1) and ((distance <= 0 or self.sector4_mute == 1) and self.playing[sensor] == 1):
            
                    # Sensor 0 (Snare)
                    if sensor == 0:
                        self.sound_midi.one_note_off(10, DATA_MIDI.C3)
                        self.sound_midi.one_note_off(10, DATA_MIDI.C3)
                        self.playing[sensor] = 0   

                    # Sensor 1 (Minor Arpeggio)
                    elif sensor == 1:
                        for s1_counter in range(5,11+1,1):
                            if self.playing[s1_counter] == 1:
                                self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[s1_counter-5+7*self.mode_1_octave_select])
                                self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[s1_counter-5+7*self.mode_1_octave_select])
                                self.arpeggio_mi_playing[s1_counter] = 0
                        self.playing[sensor] = 0  

                    # Sensor 10, 11 (Major Scale)
                    elif  sensor >= 10 and sensor <= 11:
                        if self.playing[1] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                            self.arpeggio_mi_playing[sensor] = 0
                        elif self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                        self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                        self.playing[sensor] = 0 

                    # Sensor 12 (Drum)
                    elif sensor == 12:
                        self.sound_midi.one_note_off(10, DATA_MIDI.C)
                        self.sound_midi.one_note_off(10, DATA_MIDI.C)
                        self.playing[sensor] = 0  

                    # Sensor 13 (Tom)
                    elif sensor == 13:
                        self.sound_midi.one_note_off(11, DATA_MIDI.C)
                        self.sound_midi.one_note_off(11, DATA_MIDI.C)
                        self.playing[sensor] = 0  

                    # Sensor 14 (Cymbal)
                    elif sensor == 14:
                        self.sound_midi.one_note_off(12, DATA_MIDI.C3)
                        self.sound_midi.one_note_off(12, DATA_MIDI.C3)
                        self.playing[sensor] = 0

                    # Sensor 15 (Snare)
                    elif  sensor == 15:
                        self.sound_midi.one_note_off(10, DATA_MIDI.C4)
                        self.sound_midi.one_note_off(10, DATA_MIDI.C4)
                        self.playing[sensor] = 0  

                    # Sensor 16 (Tom)
                    elif sensor == 16:
                        self.sound_midi.one_note_off(11, DATA_MIDI.C)
                        self.sound_midi.one_note_off(11, DATA_MIDI.C)
                        self.playing[sensor] = 0  

        # Mode 1 Shutdown --------------------------------------------------
        for sensor in range(0,19,1):

            # Sensor 0 (Snare)
            if sensor == 0:
                self.sound_midi.one_note_off(9, DATA_MIDI.C3)
                self.sound_midi.one_note_off(9, DATA_MIDI.C3)
                self.playing[sensor] = 0   

            # Sensor 1 (Minor Arpeggio)
            elif sensor == 1:
                for s1_counter in range(5,11+1,1):
                    if self.playing[s1_counter] == 1:
                        self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[s1_counter-5+7*self.mode_1_octave_select])
                        self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[s1_counter-5+7*self.mode_1_octave_select])
                        self.arpeggio_mi_playing[s1_counter] = 0
                self.playing[sensor] = 0  

            # Sensor 2 (Select Instrument)
            elif sensor == 2:
                self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[12+7*self.mode_1_octave_select])
                self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[12+7*self.mode_1_octave_select])
                self.playing[sensor] = 0

            # Sensor 3 (Major Arpeggio)
            elif sensor == 3:
                for s3_counter in range(5,11+1,1):
                    if self.playing[s3_counter] == 1:
                        self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[s3_counter-5+7*self.mode_1_octave_select])
                        self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[s3_counter-5+7*self.mode_1_octave_select])
                        self.arpeggio_ma_playing[s3_counter] = 0
                self.playing[sensor] = 0  

            # Sensor 4 (Select Octave)
            elif sensor == 4:
                sys.stdout.flush()
                self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[7*self.mode_1_octave_select])
                self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[7*self.mode_1_octave_select])
                self.playing[sensor] = 0

            # Sensor 5, 6, 7, 8, 9, 10, 11 (Major Scale)
            elif  sensor >= 5 and sensor <= 11:
                if self.playing[1] == 1:
                    self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                    self.sound_midi.arpeggio_mi_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                    self.arpeggio_mi_playing[sensor] = 0
                elif self.playing[3] == 1:
                    self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                    self.sound_midi.arpeggio_ma_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                self.sound_midi.one_note_off(self.mode_1_channel_select, self.Mode_1_notes[sensor-5+7*self.mode_1_octave_select])
                self.playing[sensor] = 0 

            # Sensor 12 (Drum)
            elif sensor == 12:
                self.sound_midi.one_note_off(10, DATA_MIDI.C)
                self.sound_midi.one_note_off(10, DATA_MIDI.C)
                self.playing[sensor] = 0  

            # Sensor 13 (Tom)
            elif sensor == 13:
                self.sound_midi.one_note_off(11, DATA_MIDI.C)
                self.sound_midi.one_note_off(11, DATA_MIDI.C)
                self.playing[sensor] = 0  

            # Sensor 14 (Cymbal)
            elif sensor == 14:
                self.sound_midi.one_note_off(12, DATA_MIDI.C3)
                self.sound_midi.one_note_off(12, DATA_MIDI.C3)
                self.playing[sensor] = 0 

            # Sensor 15 (Snare)
            elif  sensor == 15:
                self.sound_midi.one_note_off(10, DATA_MIDI.C4)
                self.sound_midi.one_note_off(10, DATA_MIDI.C4)
                self.playing[sensor] = 0

            # Sensor 16 (Tom)
            elif sensor == 13:
                self.sound_midi.one_note_off(11, DATA_MIDI.C)
                self.sound_midi.one_note_off(11, DATA_MIDI.C)
                self.playing[sensor] = 0  

        print('Mode 1 Shutdown')
        sys.stdout.flush()          

# --------------------------------------------------

    def mode_2(self):
        """Mode 2 function"""

        print('Start Mode 2')
        sys.stdout.flush()

        while self.sw_change is False:

            data_retrieved = self.db.select_all()

            time.sleep(0.005)

            # Switches Check --------------------------------------------------
            self.check_switches()
            
            # Previous Checks --------------------------------------------------
            for sensor, distance in data_retrieved:        

                # Check special modes --------------------------------------------------
                self.check_special_modes(sensor, distance)
                        
                # Check muted sectors --------------------------------------------------
                if 17 <= sensor <= 18:
                    self.check_mute(sensor, distance)

            for sensor, distance in data_retrieved:
                # Turn On --------------------------------------------------
                if distance > 0 and distance < 100 and self.playing[sensor] == 0:
                    if  self.sector4_mute == 0 and (0 <= sensor <= 1 or 9 <= sensor <= 14):
                        self.sound_wav.play_wav(sensor)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector3_mute == 0 and 2 <= sensor <= 9:
                        self.sound_wav.play_wav(sensor)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector4_mute == 0 and sensor == 15:
                        self.sound_wav.play_wav(0)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector4_mute == 0 and sensor == 16:
                        self.sound_wav.play_wav(13)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()

                # Turn Off --------------------------------------------------
                elif (0 <= sensor <= 1 or 9 <= sensor <= 14) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector4_mute == 1):
                    self.sound_wav.stop_wav(sensor)
                    self.playing[sensor] = 0
                elif (2 <= sensor <= 9) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector3_mute == 1):
                    self.sound_wav.stop_wav(sensor)
                    self.playing[sensor] = 0
                elif (sensor == 15) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector3_mute == 1):
                    self.sound_wav.stop_wav(0)
                    self.playing[sensor] = 0
                elif (sensor == 16) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01 and sensor == 16) or self.sector4_mute == 1):
                    self.sound_wav.stop_wav(13)
                    self.playing[sensor] = 0
        
        # Mode 2 Shutdown --------------------------------------------------
        for sensor in range(0,17,1):
            if self.playing[sensor] == 1 and 0 <= sensor <= 14:
                self.sound_wav.stop_wav(sensor)
                self.playing[sensor] = 0
            if sensor == 15:
                self.sound_wav.stop_wav(0)
                self.playing[sensor] = 0
            elif sensor == 16:
                self.sound_wav.stop_wav(13)
                self.playing[sensor] = 0

        print('Mode 2 Shutdown')
        sys.stdout.flush()

# --------------------------------------------------

    def mode_3(self):
        """Mode 3 function"""

        print('Start Mode 3')
        sys.stdout.flush()

        while self.sw_change is False:

            data_retrieved = self.db.select_all()

            time.sleep(0.005)

            # Switches Check --------------------------------------------------
            self.check_switches()
            
            # Previous Checks --------------------------------------------------
            for sensor, distance in data_retrieved:        

                # Check special modes --------------------------------------------------
                self.check_special_modes(sensor, distance)
                        
                # Check muted sectors --------------------------------------------------
                if 17 <= sensor <= 18:
                    self.check_mute(sensor, distance)

            for sensor, distance in data_retrieved:
                # Turn On --------------------------------------------------
                if distance > 0 and distance < 100 and self.playing[sensor] == 0:
                    if self.sector4_mute == 0 and (0 <= sensor <= 1 or 9 <= sensor <= 14):
                        self.sound_wav.play_wav(15+sensor)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector3_mute == 0 and 2 <= sensor <= 9:
                        self.sound_wav.play_wav(15+sensor)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector4_mute == 0 and sensor == 15:
                        self.sound_wav.play_wav(15+0)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector4_mute == 0 and sensor == 16:
                        self.sound_wav.play_wav(15+13)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()

                # Turn Off --------------------------------------------------
                elif (0 <= sensor <= 1 or 9 <= sensor <= 14) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector4_mute == 1):
                    self.sound_wav.stop_wav(15+sensor)
                    self.playing[sensor] = 0
                elif (2 <= sensor <= 9) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector3_mute == 1):
                    self.sound_wav.stop_wav(15+sensor)
                    self.playing[sensor] = 0
                elif (sensor == 15) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector3_mute == 1):
                    self.sound_wav.stop_wav(15+0)
                    self.playing[sensor] = 0
                elif (sensor == 16) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01 and sensor == 16) or self.sector4_mute == 1):
                    self.sound_wav.stop_wav(15+13)
                    self.playing[sensor] = 0
        
        # Mode 3 Shutdown --------------------------------------------------
        for sensor in range(0,17,1):
            if self.playing[sensor] == 1 and 0 <= sensor <= 14:
                self.sound_wav.stop_wav(15+sensor)
                self.playing[sensor] = 0
            if sensor == 15:
                self.sound_wav.stop_wav(15+0)
                self.playing[sensor] = 0
            elif sensor == 16:
                self.sound_wav.stop_wav(15+13)
                self.playing[sensor] = 0

        print('Mode 3 Shutdown')
        sys.stdout.flush() 

# --------------------------------------------------

    def mode_4(self):
        """Mode 4 function"""
        
        print('Start Mode 4')
        sys.stdout.flush()  

        while self.sw_change is False and self.special_mode == 0:

            data_retrieved = self.db.select_all()

            time.sleep(0.005)

            # Switches Check --------------------------------------------------
            self.check_switches()
            
            # Previous Checks --------------------------------------------------
            for sensor, distance in data_retrieved:        

                # Check special modes --------------------------------------------------
                self.check_special_modes(sensor, distance)
                        
                # Check muted sectors --------------------------------------------------
                if 17 <= sensor <= 18:
                    self.check_mute(sensor, distance)

            # Main Loop --------------------------------------------------
            for sensor, distance in data_retrieved:

                # Turn On --------------------------------------------------
                if distance > 10 and self.playing[sensor] == 0:

                    # Sensor 0 (Snare)
                    if  distance < 400 and sensor == 0 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(9, DATA_MIDI.C2, 127)
                        self.playing[sensor] = 1      

                    # Sensor 1 (Minor Arpeggio)
                    elif sensor == 1 and self.sector4_mute == 0:
                        for s1_counter in range(5,14+1,1):
                            if self.playing[s1_counter] == 1 and self.arpeggio_mi_playing[s1_counter] == 0:
                                self.sound_midi.arpeggio_mi_on(self.mode_4_channel_select, self.Mode_4_notes[s1_counter-5+5*self.mode_4_octave_select], 127)
                                self.arpeggio_mi_playing[s1_counter] = 1
                        s1_counter = 16
                        if self.playing[s1_counter] == 1 and self.arpeggio_mi_playing[s1_counter] == 0:
                            self.sound_midi.arpeggio_mi_on(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_mi_playing[s1_counter] = 1
                        self.playing[sensor] = 1

                    # Sensor 2 (Select Instrument)
                    elif sensor == 2 and self.sector3_mute == 0:
                        for s2_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s2_counter]
                            upper_bound = self.distance_vector[2*s2_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                self.sound_midi.one_note_on(s2_counter, self.Mode_4_notes[5*self.mode_4_octave_select], 127)
                                self.mode_4_channel_select = s2_counter
                        self.playing[sensor] = 1

                    # Sensor 3 (Major Arpeggio)
                    elif sensor == 3 and self.sector3_mute == 0:
                        for s3_counter in range(5,14+1,1):
                            if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                                self.sound_midi.arpeggio_ma_on(self.mode_4_channel_select, self.Mode_4_notes[s3_counter-5+5*self.mode_4_octave_select], 127)
                                self.arpeggio_ma_playing[s3_counter] = 1
                        s3_counter = 16
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] = 1
                        self.playing[sensor] = 1

                    # Sensor 4 (Select Octave)
                    elif sensor == 4 and self.sector3_mute == 0:
                        for s4_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s4_counter]
                            upper_bound = self.distance_vector[2*s4_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                self.sound_midi.one_note_on(self.mode_4_channel_select, self.Mode_4_notes[5*s4_counter], 127)
                                self.mode_4_octave_select = s4_counter
                        self.playing[sensor] = 1
                    
                    # Sensor 5, 6, 7, 8, 9 (Pentatonic Major)
                    elif distance < 400 and sensor >= 5 and sensor <= 9 and self.sector3_mute == 0:
                        self.sound_midi.one_note_on(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1
                        elif self.playing[1] == 1 and self.arpeggio_mi_playing[sensor] == 0: # Major Chord
                            self.sound_midi.arpeggio_mi_on(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_mi_playing[sensor] = 1

                    # Sensor 10, 11, 12, 13, 14 (Pentatonic Major)
                    elif distance < 400 and sensor >= 10 and sensor <= 14 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1
                        elif self.playing[1] == 1 and self.arpeggio_mi_playing[sensor] == 0: # Major Chord
                            self.sound_midi.arpeggio_mi_on(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_mi_playing[sensor] = 1

                    # Sensor 15 (Pentatonic Major)
                    elif distance < 400 and sensor == 15 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(10, DATA_MIDI.C3, 127)
                        self.playing[sensor] = 1

                    # Sensor 16 (Pentatonic Major)
                    elif distance < 400 and sensor == 16 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1
                        elif self.playing[1] == 1 and self.arpeggio_mi_playing[sensor] == 0: # Major Chord
                            self.sound_midi.arpeggio_mi_on(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_mi_playing[sensor] = 1

                # Playing --------------------------------------------------
                elif distance > 10 and self.playing[sensor] == 1 and 1 <= sensor <= 4:

                    # Sensor 1 (Minor Arpeggio)
                    if sensor == 1 and self.sector4_mute == 0:
                        for s1_counter in range(5,14+1,1):
                            if self.playing[s1_counter] == 1 and self.arpeggio_mi_playing[s1_counter] == 0:
                                self.sound_midi.arpeggio_mi_on(self.mode_4_channel_select, self.Mode_4_notes[s1_counter-5+5*self.mode_4_octave_select], 127)
                                self.arpeggio_mi_playing[s1_counter] == 1
                        s1_counter = 16
                        if self.playing[s1_counter] == 1 and self.arpeggio_mi_playing[s1_counter] == 0:
                            self.sound_midi.arpeggio_mi_on(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_mi_playing[s1_counter] == 1
                        self.playing[sensor] = 1

                    # Sensor 2 (Select Instrument)
                    elif sensor == 2 and self.sector3_mute == 0:
                        for s2_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s2_counter]
                            upper_bound = self.distance_vector[2*s2_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                if s2_counter is not self.mode_4_channel_select:
                                    self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                                    self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                                    self.sound_midi.one_note_on(s2_counter, self.Mode_4_notes[5*self.mode_4_octave_select], 127)
                                    self.mode_4_channel_select = s2_counter
                        self.playing[sensor] = 1

                    # Sensor 3 (Major Arpeggio)
                    if sensor == 3 and self.sector3_mute == 0:
                        for s3_counter in range(5,14+1,1):
                            if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                                self.sound_midi.arpeggio_ma_on(self.mode_4_channel_select, self.Mode_4_notes[s3_counter-5+5*self.mode_4_octave_select], 127)
                                self.arpeggio_ma_playing[s3_counter] == 1
                        s3_counter = 16
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] == 1
                        self.playing[sensor] = 1

                    # Sensor 4 (Select Octave)
                    elif sensor == 4 and self.sector3_mute == 0:
                        for s4_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s4_counter]
                            upper_bound = self.distance_vector[2*s4_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                if s4_counter is not self.mode_4_octave_select:
                                    self.sound_midi.notes_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                                    self.sound_midi.notes_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                                    self.sound_midi.one_note_on(self.mode_4_channel_select, self.Mode_4_notes[5*s4_counter], 127)
                                    self.mode_4_octave_select = s4_counter

                # Turn Off --------------------------------------------------
                elif (2 <= sensor <= 9 or sensor == 15) and ((distance <= 0 or self.sector3_mute == 1) and self.playing[sensor] == 1):

                    # Sensor 2 (Select Instrument)
                    if sensor == 2:
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 3 (Major Arpeggio)
                    elif sensor == 3:
                        for s3_counter in range(5,14+1,1):
                            if self.playing[s3_counter] == 1:
                                self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[s3_counter-5+5*self.mode_4_octave_select])
                                self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[s3_counter-5+5*self.mode_4_octave_select])
                                self.arpeggio_ma_playing[s3_counter] = 0
                        s3_counter = 16
                        if self.playing[s3_counter] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                            self.arpeggio_ma_playing[s3_counter] = 0
                        self.playing[sensor] = 0  

                    # Sensor 4 (Select Octave)
                    elif sensor == 4:
                        sys.stdout.flush()
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 5, 6, 7, 8, 9 (Pentatonic Major)
                    elif  sensor >= 5 and sensor <= 9:
                        if self.playing[1] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                            self.arpeggio_mi_playing[sensor] = 0
                        elif self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                        self.playing[sensor] = 0

                elif (10 <= sensor <= 14 or sensor == 16 or sensor == 0 or sensor == 1) and ((distance <= 0 or self.sector4_mute == 1) and self.playing[sensor] == 1):
            
                    # Sensor 0 (Snare)
                    if sensor == 0:
                        self.sound_midi.one_note_off(9, DATA_MIDI.C2)
                        self.sound_midi.one_note_off(9, DATA_MIDI.C2)
                        self.playing[sensor] = 0   

                    # Sensor 1 (Minor Arpeggio)
                    elif sensor == 1:
                        for s1_counter in range(5,14+1,1):
                            if self.playing[s1_counter] == 1:
                                self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[s1_counter-5+5*self.mode_4_octave_select])
                                self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[s1_counter-5+5*self.mode_4_octave_select])
                                self.arpeggio_mi_playing[s1_counter] = 0
                        s1_counter = 16
                        if self.playing[s1_counter] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                            self.arpeggio_mi_playing[s1_counter] = 0
                        self.playing[sensor] = 0  

                    # Sensor 10, 11, 12, 13, 14 (Pentatonic Major)
                    elif  sensor >= 10 and sensor <= 14:
                        if self.playing[1] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                            self.arpeggio_mi_playing[sensor] = 0
                        elif self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 15 (Pentatonic Major)
                    elif  sensor == 15:
                        self.sound_midi.one_note_off(10, DATA_MIDI.C3)
                        self.sound_midi.one_note_off(10, DATA_MIDI.C3)
                        self.playing[sensor] = 0

                    # Sensor 16 (Pentatonic Major)
                    elif  sensor == 16:
                        if self.playing[1] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                            self.arpeggio_mi_playing[sensor] = 0
                        elif self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                        self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                        self.playing[sensor] = 0

        # Mode 4 Shutdown --------------------------------------------------
        for sensor in range(0,19,1):

            # Sensor 0 (Snare)
            if sensor == 0:
                self.sound_midi.one_note_off(10, DATA_MIDI.C3)
                self.sound_midi.one_note_off(10, DATA_MIDI.C3)
                self.playing[sensor] = 0   

            # Sensor 1 (Major Chord)
            elif sensor == 1:
                for s1_counter in range(5,14+1,1):
                    if self.playing[s1_counter] == 1:
                        self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[s1_counter-5+5*self.mode_4_octave_select])
                        self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[s1_counter-5+5*self.mode_4_octave_select])
                        self.arpeggio_mi_playing[s1_counter] = 0
                self.playing[sensor] = 0  

            # Sensor 2 (Select Instrument)
            elif sensor == 2:
                self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                self.playing[sensor] = 0

            # Sensor 3 (Major Arpeggio)
            elif sensor == 3:
                for s3_counter in range(5,14+1,1):
                    if self.playing[s3_counter] == 1:
                        self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[s3_counter-5+5*self.mode_4_octave_select])
                        self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[s3_counter-5+5*self.mode_4_octave_select])
                        self.arpeggio_ma_playing[s3_counter] = 0
                self.playing[sensor] = 0  

            # Sensor 4 (Select Octave)
            elif sensor == 4:
                sys.stdout.flush()
                self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[5*self.mode_4_octave_select])
                self.playing[sensor] = 0

            # Sensor 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 (Pentatonic Major)
            elif  sensor >= 5 and sensor <= 14:
                if self.playing[1] == 1:
                    self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                    self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                    self.arpeggio_mi_playing[sensor] = 0
                elif self.playing[3] == 1:
                    self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                    self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[sensor-5+5*self.mode_4_octave_select])
                self.playing[sensor] = 0

            # Sensor 15 (Pentatonic Major)
            elif sensor == 15:
                self.sound_midi.one_note_off(10, DATA_MIDI.C3)
                self.sound_midi.one_note_off(10, DATA_MIDI.C3)
                self.playing[sensor] = 0

            # Sensor 16 (Pentatonic Major)
            elif sensor == 16:
                if self.playing[1] == 1:
                    self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                    self.sound_midi.arpeggio_mi_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                    self.arpeggio_mi_playing[sensor] = 0
                elif self.playing[3] == 1:
                    self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                    self.sound_midi.arpeggio_ma_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                self.sound_midi.one_note_off(self.mode_4_channel_select, self.Mode_4_notes[13-5+5*self.mode_4_octave_select])
                self.playing[sensor] = 0

        print('Mode 4 Shutdown')
        sys.stdout.flush()        

# --------------------------------------------------

    def mode_5(self):
        """Mode 5 function"""

        print('Start Mode 5')
        sys.stdout.flush()

        while self.sw_change is False and self.special_mode == 1:

            data_retrieved = self.db.select_all()

            time.sleep(0.005)

            # Switches Check --------------------------------------------------
            self.check_switches()
            
            # Previous Checks --------------------------------------------------
            for sensor, distance in data_retrieved:        

                # Check special modes --------------------------------------------------
                self.check_special_modes(sensor, distance)
                        
                # Check muted sectors --------------------------------------------------
                if 17 <= sensor <= 18:
                    self.check_mute(sensor, distance)

            # Main Loop --------------------------------------------------
            for sensor, distance in data_retrieved:

                # Turn On --------------------------------------------------
                if distance > 10 and self.playing[sensor] == 0:

                    # Sensor 0 (Note 11)
                    if  distance < 400 and sensor == 0 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1

                    # Sensor 1 (Note 12)
                    elif  distance < 400 and sensor == 1 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1

                    # Sensor 2 (Select Instrument)
                    elif sensor == 2 and self.sector3_mute == 0:
                        for s2_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s2_counter]
                            upper_bound = self.distance_vector[2*s2_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                self.sound_midi.one_note_on(s2_counter, self.Mode_5_notes[12*self.mode_5_octave_select], 127)
                                self.mode_5_channel_select = s2_counter
                        self.playing[sensor] = 1

                    # Sensor 3 (Major Arpeggio)
                    elif sensor == 3 and self.sector3_mute == 0:
                        for s3_counter in range(5,14+1,1):
                            if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                                self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[s3_counter-5+12*self.mode_5_octave_select], 127)
                                self.arpeggio_ma_playing[s3_counter] = 1
                        s3_counter = 0
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] = 1
                        s3_counter = 1
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] = 1
                        s3_counter = 15
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] = 1
                        s3_counter = 16
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] = 1
                        self.playing[sensor] = 1

                    # Sensor 4 (Select Octave)
                    elif sensor == 4 and self.sector3_mute == 0:
                        for s4_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s4_counter]
                            upper_bound = self.distance_vector[2*s4_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                self.sound_midi.one_note_on(self.mode_5_channel_select, self.Mode_5_notes[12*s4_counter], 127)
                                self.mode_5_octave_select = s4_counter
                        self.playing[sensor] = 1
                    
                    # Sensor 5, 6, 7, 8, 9 (Scale)
                    elif distance < 400 and sensor >= 5 and sensor <= 9 and self.sector3_mute == 0:
                        self.sound_midi.one_note_on(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1

                    # Sensor 10, 11, 12, 13, 14 (Scale)
                    elif distance < 400 and sensor >= 10 and sensor <= 14 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1

                    # Sensor 15 (Note 11)
                    if  distance < 400 and sensor == 15 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1

                    # Sensor 16 (Note 8)
                    elif  distance < 400 and sensor == 16 and self.sector4_mute == 0:
                        self.sound_midi.one_note_on(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1

                # Playing --------------------------------------------------
                elif distance > 10 and self.playing[sensor] == 1 and 2 <= sensor <= 4:

                    # Sensor 2 (Select Instrument)
                    if sensor == 2 and self.sector3_mute == 0:
                        for s2_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s2_counter]
                            upper_bound = self.distance_vector[2*s2_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                if s2_counter is not self.mode_5_channel_select:
                                    self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                                    self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                                    self.sound_midi.one_note_on(s2_counter, self.Mode_5_notes[12*self.mode_5_octave_select], 127)
                                    self.mode_5_channel_select = s2_counter
                        self.playing[sensor] = 1

                    # Sensor 3 (Major Arpeggio)
                    if sensor == 3 and self.sector3_mute == 0:
                        for s3_counter in range(5,14+1,1):
                            if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                                self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[s3_counter-5+12*self.mode_5_octave_select], 127)
                                self.arpeggio_ma_playing[s3_counter] == 1
                        s3_counter = 0
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] == 1
                        s3_counter = 1
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] == 1
                        s3_counter = 15
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] == 1
                        s3_counter = 16
                        if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                            self.sound_midi.arpeggio_ma_on(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select], 127)
                            self.arpeggio_ma_playing[s3_counter] == 1
                        self.playing[sensor] = 1

                    # Sensor 4 (Select Octave)
                    elif sensor == 4 and self.sector3_mute == 0:
                        for s4_counter in range(int(len(self.distance_vector)/2-1)):
                            lower_bound = self.distance_vector[2*s4_counter]
                            upper_bound = self.distance_vector[2*s4_counter+1]
                            if distance > lower_bound and distance < upper_bound:
                                if s4_counter is not self.mode_5_octave_select:
                                    self.sound_midi.notes_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                                    self.sound_midi.notes_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                                    self.sound_midi.one_note_on(self.mode_5_channel_select, self.Mode_5_notes[12*s4_counter], 127)
                                    self.mode_5_octave_select = s4_counter
                        self.playing[sensor] = 1

                # Turn Off --------------------------------------------------
                elif (2 <= sensor <= 9) and ((distance <= 0 or self.sector3_mute == 1) and self.playing[sensor] == 1):

                    # Sensor 2 (Select Instrument)
                    if sensor == 2:
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 3 (Major Arpeggio)
                    elif sensor == 3:
                        for s3_counter in range(5,14+1,1):
                            if self.playing[s3_counter] == 1:
                                self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[s3_counter-5+12*self.mode_5_octave_select])
                                self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[s3_counter-5+12*self.mode_5_octave_select])
                                self.arpeggio_ma_playing[s3_counter] = 0
                        s3_counter = 0
                        if self.playing[s3_counter] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[s3_counter] = 0
                        s3_counter = 1
                        if self.playing[s3_counter] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[s3_counter] = 0
                        s3_counter = 15
                        if self.playing[s3_counter] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[s3_counter] = 0
                        s3_counter = 16
                        if self.playing[s3_counter] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[s3_counter] = 0
                        self.playing[sensor] = 0  

                    # Sensor 4 (Select Octave)
                    elif sensor == 4:
                        sys.stdout.flush()
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 5, 6, 7, 8, 9 (Scale)
                    elif  sensor >= 5 and sensor <= 9:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                        self.playing[sensor] = 0

                elif (10 <= sensor <= 14 or sensor == 15 or sensor == 16 or sensor == 0 or sensor == 1) and ((distance <= 0 or self.sector4_mute == 1) and self.playing[sensor] == 1):
            
                    # Sensor 0 (Note 11)
                    if sensor == 0:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                        self.playing[sensor] = 0 

                    # Sensor 1 (Note 12)
                    elif sensor == 1:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                        self.playing[sensor] = 0 

                    # Sensor 10, 11, 12, 13, 14 (Scale)
                    elif  sensor >= 10 and sensor <= 14:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 15 (Note 11)
                    elif sensor == 15:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                        self.playing[sensor] = 0 

                    # Sensor 16 (Note 8)
                    elif sensor == 16:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                            self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                        self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                        self.playing[sensor] = 0 

        # Mode 5 Shutdown --------------------------------------------------
        for sensor in range(0,19,1):

            # Sensor 0 (Note 11)
            if sensor == 0:
                if self.playing[3] == 1:
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                self.playing[sensor] = 0  

            # Sensor 1 (Note 12)
            elif sensor == 1:
                if self.playing[3] == 1:
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[11+12*self.mode_5_octave_select])
                self.playing[sensor] = 0  

            # Sensor 2 (Select Instrument)
            elif sensor == 2:
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                self.playing[sensor] = 0

            # Sensor 3 (Major Arpeggio)
            elif sensor == 3:
                for s3_counter in range(5,14+1,1):
                    if self.playing[s3_counter] == 1:
                        self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[s3_counter-5+12*self.mode_5_octave_select])
                        self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[s3_counter-5+12*self.mode_5_octave_select])
                        self.arpeggio_ma_playing[s3_counter] = 0
                self.playing[sensor] = 0  

            # Sensor 4 (Select Octave)
            elif sensor == 4:
                sys.stdout.flush()
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[12*self.mode_5_octave_select])
                self.playing[sensor] = 0

            # Sensor 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 (Scale)
            elif  sensor >= 5 and sensor <= 14:
                if self.playing[3] == 1:
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[sensor-5+12*self.mode_5_octave_select])
                self.playing[sensor] = 0

            # Sensor 15 (Note 11)
            if sensor == 15:
                if self.playing[3] == 1:
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[10+12*self.mode_5_octave_select])
                self.playing[sensor] = 0  

            # Sensor 16 (Note 8)
            elif sensor == 16:
                if self.playing[3] == 1:
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                    self.sound_midi.arpeggio_ma_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                self.sound_midi.one_note_off(self.mode_5_channel_select, self.Mode_5_notes[13-5+12*self.mode_5_octave_select])
                self.playing[sensor] = 0 

        print('Mode 5 Shutdown')
        sys.stdout.flush() 

# --------------------------------------------------

    def mode_6(self):
        """Mode 6 function"""

        print('Start Mode 6')
        sys.stdout.flush()

        while self.sw_change is False and self.special_mode == 1:

            data_retrieved = self.db.select_all()

            time.sleep(0.005)

            # Switches Check --------------------------------------------------
            self.check_switches()
            
            # Previous Checks --------------------------------------------------
            for sensor, distance in data_retrieved:        

                # Check special modes --------------------------------------------------
                self.check_special_modes(sensor, distance)
                        
                # Check muted sectors --------------------------------------------------
                if 17 <= sensor <= 18:
                    self.check_mute(sensor, distance)

            # Main Loop --------------------------------------------------
            for sensor, distance in data_retrieved:

                # Turn On --------------------------------------------------
                if distance > 10 and self.playing[sensor] == 0:

                    # Sensor 0 (Note 11)
                    if  distance < 400 and sensor == 0:
                        self.sound_midi.one_note_on(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_mi_on(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1 

                    # Sensor 1 (Note 12)
                    if  distance < 400 and sensor == 1:
                        self.sound_midi.one_note_on(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_mi_on(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1

                    # Sensor 2 (Select Instrument)
                    elif sensor == 2:
                        for s2_counter in range(len(self.distance_vector)-1):
                            if distance > self.distance_vector[s2_counter] and distance < self.distance_vector[s2_counter+1]:
                                self.sound_midi.one_note_on(s2_counter, self.Mode_6_notes[12*self.mode_6_octave_select], 127)
                                self.mode_6_channel_select = s2_counter
                        self.playing[sensor] = 1

                    # Sensor 3 (Minor Arpeggio)
                    elif sensor == 3:
                        for s3_counter in range(5,12,1):
                            if self.playing[s3_counter] == 1:
                                self.sound_midi.arpeggio_mi_on(self.mode_6_channel_select, self.Mode_6_notes[s3_counter-5+12*self.mode_6_octave_select], 127)
                                self.arpeggio_ma_playing[s3_counter] = 1
                        self.playing[sensor] = 1

                    # Sensor 4 (Select Octave)
                    elif sensor == 4:
                        for s4_counter in range(len(self.distance_vector)-1):
                            if distance > self.distance_vector[s4_counter] and distance < self.distance_vector[s4_counter+1]:
                                self.sound_midi.one_note_on(self.mode_6_channel_select, self.Mode_6_notes[12*s4_counter], 127)
                                self.mode_6_octave_select = s4_counter
                        self.playing[sensor] = 1
                    
                    # Sensor 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 (Scale)
                    elif distance < 400 and sensor >= 5 and sensor <= 14:
                        self.sound_midi.one_note_on(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select], 127)
                        self.playing[sensor] = 1
                        if self.playing[3] == 1 and self.arpeggio_ma_playing[sensor] == 0: # Major Arpeggio
                            self.sound_midi.arpeggio_mi_on(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select], 127)
                            self.arpeggio_ma_playing[sensor] = 1

                # Playing --------------------------------------------------
                elif distance > 10 and self.playing[sensor] == 1 and 2 <= sensor <= 4:

                    # Sensor 2 (Select Instrument)
                    if sensor == 2:
                        for s2_counter in range(len(self.distance_vector)-1):
                            if distance > self.distance_vector[s2_counter] and distance < self.distance_vector[s2_counter+1]:
                                if s2_counter is not self.mode_6_channel_select:
                                    self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                                    self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                                    self.sound_midi.one_note_on(s2_counter, self.Mode_6_notes[12*self.mode_5_octave_select], 127)
                                    self.mode_6_channel_select = s2_counter

                    # Sensor 3 (Major Arpeggio)
                    if sensor == 3:
                        for s3_counter in range(5,12,1):
                            if self.playing[s3_counter] == 1 and self.arpeggio_ma_playing[s3_counter] == 0:
                                self.sound_midi.arpeggio_mi_on(self.mode_6_channel_select, self.Mode_6_notes[s3_counter-5+12*self.mode_6_octave_select], 127)
                                self.arpeggio_ma_playing[s3_counter] == 1
                        self.playing[sensor] = 1

                    # Sensor 4 (Select Octave)
                    elif sensor == 4:
                        for s4_counter in range(len(self.distance_vector)-1):
                            if distance > self.distance_vector[s4_counter] and distance < self.distance_vector[s4_counter+1]:
                                if s4_counter is not self.mode_6_octave_select:
                                    self.sound_midi.notes_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                                    self.sound_midi.notes_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                                    self.sound_midi.one_note_on(self.mode_6_channel_select, self.Mode_6_notes[12*s4_counter], 127)
                                    self.mode_6_octave_select = s4_counter

                # Turn Off --------------------------------------------------
                elif distance <= 0 and self.playing[sensor] == 1:
        
                    # Sensor 0 (Note 11)
                    if sensor == 0:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select])
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select])
                        self.playing[sensor] = 0  

                    # Sensor 1 (Note 12)
                    if sensor == 0:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select])
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select])
                        self.playing[sensor] = 0  

                    # Sensor 2 (Select Instrument)
                    elif sensor == 2:
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 3 (Major Arpeggio)
                    elif sensor == 3:
                        for s3_counter in range(5,12,1):
                            if self.playing[s3_counter] == 1:
                                self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[s3_counter-5+12*self.mode_6_octave_select])
                                self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[s3_counter-5+12*self.mode_6_octave_select])
                                self.arpeggio_ma_playing[s3_counter] = 0
                        self.playing[sensor] = 0  

                    # Sensor 4 (Select Octave)
                    elif sensor == 4:
                        sys.stdout.flush()
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                        self.playing[sensor] = 0

                    # Sensor 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 (Scale)
                    elif  sensor >= 5 and sensor <= 14:
                        if self.playing[3] == 1:
                            self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select])
                            self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select])
                            self.arpeggio_ma_playing[sensor] = 0
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select])
                        self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select])
                        self.playing[sensor] = 0 

        # Mode 6 Shutdown --------------------------------------------------
        for sensor in range(0,19,1):

            # Sensor 0 (Note 11)
            if sensor == 0:
                if self.playing[3] == 1:
                    self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select])
                    self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select])
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[11+12*self.mode_6_octave_select])
                self.playing[sensor] = 0  

            # Sensor 1 (Major Chord)
            elif sensor == 1:
                if self.playing[3] == 1:
                    self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select])
                    self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select])
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12+12*self.mode_6_octave_select])
                self.playing[sensor] = 0  

            # Sensor 2 (Select Instrument)
            elif sensor == 2:
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                self.playing[sensor] = 0

            # Sensor 3 (Major Arpeggio)
            elif sensor == 3:
                for s3_counter in range(5,12,1):
                    if self.playing[s3_counter] == 1:
                        self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[s3_counter-5+12*self.mode_6_octave_select])
                        self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[s3_counter-5+12*self.mode_6_octave_select])
                        self.arpeggio_ma_playing[s3_counter] = 0
                self.playing[sensor] = 0  

            # Sensor 4 (Select Octave)
            elif sensor == 4:
                sys.stdout.flush()
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[12*self.mode_6_octave_select])
                self.playing[sensor] = 0

            # Sensor 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 (Scale)
            elif  sensor >= 5 and sensor <= 14:
                if self.playing[3] == 1:
                    self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select])
                    self.sound_midi.arpeggio_mi_off(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select])
                    self.arpeggio_ma_playing[sensor] = 0
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select])
                self.sound_midi.one_note_off(self.mode_6_channel_select, self.Mode_6_notes[sensor-5+12*self.mode_6_octave_select])
                self.playing[sensor] = 0 

        print('Mode 6 Shutdown')
        sys.stdout.flush() 

# --------------------------------------------------

    def mode_7(self):
        """Mode 7 function"""

        print('Start Mode 7')
        sys.stdout.flush()

        while self.sw_change is False:

            data_retrieved = self.db.select_all()

            time.sleep(0.005)

            # Switches Check --------------------------------------------------
            self.check_switches()
            
            # Previous Checks --------------------------------------------------
            for sensor, distance in data_retrieved:        

                # Check special modes --------------------------------------------------
                self.check_special_modes(sensor, distance)
                        
                # Check muted sectors --------------------------------------------------
                if 17 <= sensor <= 18:
                    self.check_mute(sensor, distance)

            for sensor, distance in data_retrieved:
                # Turn On --------------------------------------------------
                if distance > 0 and distance < 100 and self.playing[sensor] == 0:
                    if self.sector4_mute == 0 and (0 <= sensor <= 1 or 9 <= sensor <= 14):
                        self.sound_wav.play_wav(30+sensor)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector3_mute == 0 and 2 <= sensor <= 9:
                        self.sound_wav.play_wav(30+sensor)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector4_mute == 0 and sensor == 15:
                        self.sound_wav.play_wav(30+0)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()
                    elif self.sector4_mute == 0 and sensor == 16:
                        self.sound_wav.play_wav(30+13)
                        self.playing[sensor] = 1
                        self.mode_2_timer[sensor] = time.monotonic()

                # Turn Off --------------------------------------------------
                elif (0 <= sensor <= 1 or 9 <= sensor <= 14) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector4_mute == 1):
                    self.sound_wav.stop_wav(30+sensor)
                    self.playing[sensor] = 0
                elif (2 <= sensor <= 9) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector3_mute == 1):
                    self.sound_wav.stop_wav(30+sensor)
                    self.playing[sensor] = 0
                elif (sensor == 15) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01) or self.sector3_mute == 1):
                    self.sound_wav.stop_wav(30+0)
                    self.playing[sensor] = 0
                elif (sensor == 16) and ((distance <= 0 and self.playing[sensor] == 1 and self.mode_2_timer[sensor]+self.WAV_length[sensor] <= time.monotonic()+0.01 and sensor == 16) or self.sector4_mute == 1):
                    self.sound_wav.stop_wav(30+13)
                    self.playing[sensor] = 0
        
        # Mode 7 Shutdown --------------------------------------------------
        for sensor in range(0,17,1):
            if self.playing[sensor] == 1 and 0 <= sensor <= 14:
                self.sound_wav.stop_wav(30+sensor)
                self.playing[sensor] = 0
            if sensor == 15:
                self.sound_wav.stop_wav(30+0)
                self.playing[sensor] = 0
            elif sensor == 16:
                self.sound_wav.stop_wav(30+13)
                self.playing[sensor] = 0

        print('Mode 7 Shutdown')
        sys.stdout.flush() 

# --------------------------------------------------

    def switch_0_change_cb(self, *args):
        """Callback that comes up when a change in the status of the switch 0 is detected"""

        self.sw_change = True
        self.special_mode = 0

# --------------------------------------------------

    def switch_1_change_cb(self, *args):
        """Callback that comes up when a change in the status of the switch 1 is detected"""

        self.sw_change = True
        self.special_mode = 0

# --------------------------------------------------

if __name__ == "__main__":
    # Ultrasonic Sensors Initialization
    ultra = Ultrasonic()
    #ultra_process = mp.Process(target=ultra.ultrasonic_main_filter_3_new_2, args=())
    #ultra_process = mp.Process(target=ultra.ultrasonic_main_filter_3, args=())
    ultra_process = mp.Process(target=ultra.ultrasonic_main_filter_4, args=())
    ultra_process.start()
    time.sleep(0.1)

    music = Music()
    music.main_final()

# --------------------------------------------------
