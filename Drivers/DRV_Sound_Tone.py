# --------------------------------------------------

"""Driver to control tone reproduction"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import numpy
import pygame
import time
import Drivers.Values_Tone as DATA

# --------------------------------------------------

class Sound_Tone():
    """Sound reproduction functions"""

# --------------------------------------------------

    def  __init__(self):
        """Initialization"""

        # Variable initialization
        self.sample_rate = 44100 #for analog audio
        self.bits_per_sample = -16 #16 bits
        self.channels = 2 #stereo
        self.buffer_size = 512
        self.max_time = 0.050 #time between different measurements

        # Mixer Initialization
        pygame.mixer.init(frequency=self.sample_rate, size=self.bits_per_sample, channels=self.channels, buffer=self.buffer_size)
        pygame.mixer.set_num_channels(20)

        # Tone Generation
        self.array = ["" for i in range(len(DATA.NOTES))]
        self.generate_all_tones_2()

# --------------------------------------------------

    def generate_all_tones(self):
        """Function that creates all the tones that might be used"""
        for i in range(len(DATA.NOTES)):
            arr = numpy.array([4096 * numpy.sin(2.0 * numpy.pi * DATA.NOTES[i] * x / self.sample_rate) for x in range(0, self.sample_rate)]).astype(numpy.int16)
            arr2 = numpy.c_[arr, arr]
            sound_mixer = pygame.mixer.Sound(arr2)
            self.array[i] = sound_mixer

# --------------------------------------------------

    def generate_all_tones_2(self):
        """Function that creates all the tones that might be used"""
        i = 20
        arr = numpy.array([4096 * numpy.sin(2.0 * numpy.pi * DATA.NOTES[i] * x / self.sample_rate) for x in range(0, self.sample_rate)]).astype(numpy.int16)
        arr2 = numpy.c_[arr, arr]
        sound_mixer = pygame.mixer.Sound(arr2)
        self.array[i] = sound_mixer

# --------------------------------------------------

    def all_start_tones(self):
        """Function that starts playing all tones"""
        for i in range(len(DATA.NOTES)):
            self.array[i].play(loops=-1, maxtime=0, fade_ms=0)
            self.one_set_volume(0.0, i)

# --------------------------------------------------

    def all_stop_tones(self):
        """Function that stops playing all tones"""
        for i in range(len(DATA.NOTES)):
            self.array[i].stop()

# --------------------------------------------------

    def one_start(self, pos):
        """Function that starts playing one tone"""
        self.array[pos].play(loops=-1, maxtime=0, fade_ms=0)
        self.one_set_volume(0.0, pos)

# --------------------------------------------------

    def one_stop(self, pos):
        """Function that stops playing one tone"""
        self.one_lower_volume(0.0, pos)
        self.array[pos].stop()

# --------------------------------------------------

    def one_set_volume(self, desired_volume, pos):
        """Function that sets the volume of a determined tone"""
        pygame.mixer.Sound.set_volume(self.array[pos], desired_volume)

# --------------------------------------------------

    def one_rise_volume(self, desired_volume, pos):
        """Function that makes smooth upward volume transitions"""
        current_volume = pygame.mixer.Sound.get_volume(self.array[pos])
        time_sleep = -self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Sound.set_volume(self.array[pos], j/100)
            time.sleep(time_sleep)
        pygame.mixer.Sound.set_volume(self.array[pos], desired_volume)

# --------------------------------------------------

    def one_lower_volume(self, desired_volume, pos):
        """Function that makes smooth downward volume transitions"""
        current_volume = pygame.mixer.Sound.get_volume(self.array[pos])
        time_sleep = self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Sound.set_volume(self.array[pos], j/100)
            time.sleep(time_sleep)
        pygame.mixer.Sound.set_volume(self.array[pos], desired_volume)

# --------------------------------------------------

    def chord_ma_start(self, pos):
        """Function that turns on a Chord using Note as the Root"""
        self.array[pos+DATA.MAJOR_CHORD[1]].play(loops=-1, maxtime=0, fade_ms=0)
        self.one_set_volume(0.0, pos)
        self.array[pos+DATA.MAJOR_CHORD[2]].play(loops=-1, maxtime=0, fade_ms=0)
        self.one_set_volume(0.0, pos)

# --------------------------------------------------

    def chord_ma_stop(self, pos):
        """Function that stops playing a Chord using Note as the Root"""
        current_volume = pygame.mixer.Sound.get_volume(self.array[pos+DATA.MAJOR_CHORD[0]])
        desired_volume = 0.0
        time_sleep = -self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[1]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[2]], j/100)
            time.sleep(time_sleep)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[1]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[2]], desired_volume)
        self.array[pos+DATA.MAJOR_CHORD[1]].stop()
        self.array[pos+DATA.MAJOR_CHORD[2]].stop()

# --------------------------------------------------

    def chord_ma_set_volume(self, desired_volume, pos):
        """Function that sets the volume of a determined Chord"""
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[0]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[1]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[2]], desired_volume)

# --------------------------------------------------

    def chord_ma_rise_volume(self, desired_volume, pos):
        """Function that turns on a Chord using Note as the Root"""
        current_volume = pygame.mixer.Sound.get_volume(self.array[pos+DATA.MAJOR_CHORD[0]])
        time_sleep = -self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[0]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[1]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[2]], j/100)
            time.sleep(time_sleep)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[0]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[1]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[2]], desired_volume)

# --------------------------------------------------

    def chord_ma_lower_volume(self, desired_volume, pos):
        """Function that turns on a Chord using Note as the Root"""
        current_volume = pygame.mixer.Sound.get_volume(self.array[pos+DATA.MAJOR_CHORD[0]])
        time_sleep = self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[0]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[1]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[2]], j/100)
            time.sleep(time_sleep)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[0]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[1]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MAJOR_CHORD[2]], desired_volume)

# --------------------------------------------------

    def chord_mi_start(self, pos):
        """Function that turns on a Chord using Note as the Root"""
        self.array[pos+DATA.MINOR_CHORD[1]].play(loops=-1, maxtime=0, fade_ms=0)
        self.one_set_volume(0.0, pos)
        self.array[pos+DATA.MINOR_CHORD[2]].play(loops=-1, maxtime=0, fade_ms=0)
        self.one_set_volume(0.0, pos)

# --------------------------------------------------

    def chord_mi_stop(self, pos):
        """Function that stops playing a Chord using Note as the Root"""
        current_volume = pygame.mixer.Sound.get_volume(self.array[pos+DATA.MINOR_CHORD[0]])
        desired_volume = 0.0
        time_sleep = -self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[1]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[2]], j/100)
            time.sleep(time_sleep)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[1]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[2]], desired_volume)
        self.array[pos+DATA.MINOR_CHORD[1]].stop()
        self.array[pos+DATA.MINOR_CHORD[2]].stop()

# --------------------------------------------------

    def chord_mi_set_volume(self, desired_volume, pos):
        """Function that sets the volume of a determined Chord"""
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[0]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[1]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[2]], desired_volume)

# --------------------------------------------------

    def chord_mi_rise_volume(self, desired_volume, pos):
        """Function that rises the volume of a Chord using Note as the Root"""
        current_volume = pygame.mixer.Sound.get_volume(self.array[pos+DATA.MINOR_CHORD[0]])
        time_sleep = -self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[0]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[1]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[2]], j/100)
            time.sleep(time_sleep)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[0]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[1]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[2]], desired_volume)

# --------------------------------------------------

    def chord_mi_lower_volume(self, desired_volume, pos):
        """Function that lowers the volume of a Chord using Note as the Root"""
        current_volume = pygame.mixer.Sound.get_volume(self.array[pos+DATA.MINOR_CHORD[0]])
        time_sleep = self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[0]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[1]], j/100)
            pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[2]], j/100)
            time.sleep(time_sleep)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[0]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[1]], desired_volume)
        pygame.mixer.Sound.set_volume(self.array[pos+DATA.MINOR_CHORD[2]], desired_volume)

# --------------------------------------------------

if __name__ == "__main__":
    sound_tone = Sound_Tone()
    print("Done")
    time.sleep(1)

    while True:
        sound_tone.one_start(20)
        sound_tone.chord_ma_start(20)
        sound_tone.chord_ma_rise_volume(0.5, 20)
        sound_tone.chord_ma_set_volume(0.5, 20)
        time.sleep(2)
        sound_tone.chord_ma_rise_volume(1.0, 20)
        time.sleep(2)
        sound_tone.chord_ma_set_volume(1.0, 20)
        time.sleep(2)
        sound_tone.chord_ma_lower_volume(0.5, 20)
        time.sleep(2)
        sound_tone.chord_ma_set_volume(0.5, 20)
        time.sleep(2)
        sound_tone.chord_ma_stop(20)
        time.sleep(2)
        sound_tone.one_rise_volume(1.0, 20)
        time.sleep(2)
        sound_tone.one_set_volume(1.0, 20)
        time.sleep(2)
        sound_tone.one_stop(20)
        time.sleep(2)

"""
    while True:
        for x in range(10, 24, 1):
            print(x)
            sound_tone.one_start_tone(x)
            sound_tone.one_set_volume(1.0, x)
            time.sleep(3)
            sound_tone.one_lower_volume(0.5, x)
            sound_tone.one_set_volume(0.5, x)
            time.sleep(3)
            sound_tone.one_rise_volume(1.0, x)
            time.sleep(3)
            sound_tone.one_lower_volume(0.2, x)
            sound_tone.one_set_volume(0.2, x)
            #sound_tone.one_stop_tone(x)
"""
# --------------------------------------------------
