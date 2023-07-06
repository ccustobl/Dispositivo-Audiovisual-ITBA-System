# --------------------------------------------------

"""Driver to control sound reproduction"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import subprocess
import shlex
import time
import sys
import pygame
import pygame.midi
import Drivers.Values_MIDI as DATA
#import Values_MIDI as DATA

# --------------------------------------------------

class Sound_MIDI():
    """Sound reproduction functions"""

# --------------------------------------------------

    def  __init__(self):
        """Initialization"""
        # Variable initialization
        self._note_volume = {} # Max volume is velocity=127
        self._note_status = {} # 1 for ON, 0 for OFF
        self._port = 3
        self._latency = 1 # Delay between input and output
        self._base_note_standard = DATA.C2 # Do/C Standard is 60, C4
        self._base_note = self._base_note_standard
        self._base_note_old = self._base_note
        self._instrument_selected = 0
        self._instrument_counter = 0

        # MIDI Server
        command_line = "timidity -iA"
        args = shlex.split(command_line)
        subprocess.Popen(args)
        time.sleep(5)

        # Pygame initialization
        pygame.init()
        pygame.midi.init()
        # Check MIDI Devices
        #for x in range( 0, pygame.midi.get_count() ):
        #    print pygame.midi.get_device_info(x)
        #print pygame.midi.get_default_output_id()
        self.midi_output = pygame.midi.Output(self._port, self._latency)
        #self.midi_output.set_instrument(self._instrument_selected, channel=1)
        #self.midi_output.set_instrument(6, channel=0)
        #self.midi_output.set_instrument(16, channel=1)
        #self.midi_output.set_instrument(116, channel=2)
        #self.midi_output.set_instrument(116, channel=3)
        #self.midi_output.set_instrument(68, channel=4)
        #self.midi_output.set_instrument(6, channel=5)

# --------------------------------------------------

    def arpeggio_ma_on(self, instrument, note, velocity):
        """Function that turns on an Arpeggio using Note as the Root"""
        self.midi_output.note_on(self._base_note+note+DATA.MAJOR_ARP[0], velocity, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MAJOR_ARP[1], velocity-40, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MAJOR_ARP[2], velocity-40, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MAJOR_ARP[3], velocity-40, channel=instrument)

# --------------------------------------------------

    def arpeggio_ma_off(self, instrument, note):
        """Function that turns off an Arpeggio using Note as the Root"""
        self.midi_output.note_off(self._base_note+note+DATA.MAJOR_ARP[0], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MAJOR_ARP[1], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MAJOR_ARP[2], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MAJOR_ARP[3], velocity=0, channel=instrument)

# --------------------------------------------------

    def chord_ma_on(self, instrument, note, velocity):
        """Function that turns on a Chord using Note as the Root"""
        self.midi_output.note_on(self._base_note+note+DATA.MAJOR_CHORD[0], velocity, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MAJOR_CHORD[1], velocity, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MAJOR_CHORD[2], velocity, channel=instrument)

# --------------------------------------------------

    def chord_ma_off(self, instrument, note):
        """Function that turns off a Chord using Note as the Root"""
        self.midi_output.note_off(self._base_note+note+DATA.MAJOR_CHORD[0], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MAJOR_CHORD[1], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MAJOR_CHORD[2], velocity=0, channel=instrument)

# --------------------------------------------------

    def arpeggio_mi_on(self, instrument, note, velocity):
        """Function that turns on an Arpeggio using Note as the Root"""
        self.midi_output.note_on(self._base_note+note+DATA.MINOR_ARP[0], velocity, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MINOR_ARP[1], velocity-40, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MINOR_ARP[2], velocity-40, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MINOR_ARP[3], velocity-40, channel=instrument)

# --------------------------------------------------

    def arpeggio_mi_off(self, instrument, note):
        """Function that turns off an Arpeggio using Note as the Root"""
        self.midi_output.note_off(self._base_note+note+DATA.MINOR_ARP[0], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MINOR_ARP[1], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MINOR_ARP[2], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MINOR_ARP[3], velocity=0, channel=instrument)

# --------------------------------------------------

    def chord_mi_on(self, instrument, note, velocity):
        """Function that turns on a Chord using Note as the Root"""
        self.midi_output.note_on(self._base_note+note+DATA.MINOR_CHORD[0], velocity-40, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MINOR_CHORD[1], velocity-40, channel=instrument)
        self.midi_output.note_on(self._base_note+note+DATA.MINOR_CHORD[2], velocity-40, channel=instrument)

# --------------------------------------------------

    def chord_mi_off(self, instrument, note):
        """Function that turns off a Chord using Note as the Root"""
        self.midi_output.note_off(self._base_note+note+DATA.MINOR_CHORD[0], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MINOR_CHORD[1], velocity=0, channel=instrument)
        self.midi_output.note_off(self._base_note+note+DATA.MINOR_CHORD[2], velocity=0, channel=instrument)

# --------------------------------------------------

    def notes_off(self, instrument, note):
        """Function that turns off all the notes related to Base_Note"""
        for counter in range (12):
            self.midi_output.note_off(note+counter, velocity=127, channel=instrument)

# --------------------------------------------------

    def all_notes_off(self, instrument):
        """Function that turns off all the notes related to Base_Note"""
        for counter in range (120):
            self.midi_output.note_off(counter, velocity=127, channel=instrument)

# --------------------------------------------------

    def one_note_on(self, instrument, note, velocity):
        """Function that turns on a single Note"""
        self.midi_output.note_on(self._base_note+note, velocity, channel=instrument)

# --------------------------------------------------

    def one_note_off(self, instrument, note):
        """Function that turns off a single Note"""
        self.midi_output.note_off(self._base_note+note, velocity=127, channel=instrument)

# --------------------------------------------------

    def set_instrument_and_channel(self, instrument, channel):
        """Function that changes the instrument in the desired channel"""
        self.midi_output.set_instrument(instrument, channel)

# --------------------------------------------------

if __name__ == "__main__":

    #command_line = "timidity -iA"
    #args = shlex.split(command_line)
    #subprocess.Popen(args)
    #time.sleep(5)
    #print('done')
    sound = Sound_MIDI()
    """
    # Test 1

    vector = [C4, D4, E4, F4, G4, A4, B4, C5]

    # Startup Routine
    for x in range(34, 40):
        print(x)
        time.sleep(1)
        sound.midi_output.set_instrument(x, channel=1)

        #Rise
        for y in range(0, 8):
            sound.midi_output.note_on(vector[y], velocity=127, channel=1)
            time.sleep(1)
            sound.midi_output.note_off(vector[y], velocity=127, channel=1)

    # Test 2
    sound.midi_output.set_instrument(16, channel=0)
    sound.midi_output.note_on(C4, velocity=127, channel=0)
    time.sleep(1)
    sound.midi_output.set_instrument(78, channel=1)
    sound.midi_output.note_on(C4, velocity=127, channel=1)
    time.sleep(1)
    sound.midi_output.set_instrument(0, channel=2)
    sound.midi_output.note_on(C4, velocity=127, channel=2)
    time.sleep(1)
    sound.midi_output.set_instrument(104, channel=3)
    sound.midi_output.note_on(C4, velocity=127, channel=3)
    time.sleep(1)
    sound.midi_output.set_instrument(23, channel=4)
    sound.midi_output.note_on(C4, velocity=127, channel=4)
    time.sleep(10)
    """

    # Test 3
    for value in range(16,127,1):
        sound.set_instrument_and_channel(value, 1)
        time.sleep(0.1)
        sound.midi_output.note_on(60, velocity=127, channel=1)
        print(value)
        sys.stdout.flush()
        time.sleep(0.2)
        sound.midi_output.note_off(60, velocity=0, channel=1)
        time.sleep(5)
        sound.midi_output.note_on(60, velocity=127, channel=1)
        print(value)
        sys.stdout.flush()
        time.sleep(0.2)
        sound.midi_output.note_off(60, velocity=127, channel=1)
        time.sleep(5)
    time.sleep(10)
    sound.midi_output.close()


# --------------------------------------------------
