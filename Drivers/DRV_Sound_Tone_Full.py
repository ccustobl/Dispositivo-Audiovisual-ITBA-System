# --------------------------------------------------

"""Driver to control full tone modulation reproduction"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import time
import numpy
import pygame
import Drivers.Values_Tone as DATA

# --------------------------------------------------

class Sound_Tone_Full():
    """Sound reproduction functions"""

# --------------------------------------------------

    def  __init__(self, initial_freq, final_freq):
        """Initialization"""

        # Variable Initialization
        self.max_time = 0.050 #time between different measurements
        self.tone_duration = 0.010
        self.currently_playing = 0
        self.next_in_queue = 0

        # Mixer Initialization
        sample_rate = 44100 # for analog audio
        bits_per_sample = -16 # 16 bits
        channels = 2 # stereo
        buffer_size = 512
        pygame.mixer.init(frequency=sample_rate, size=bits_per_sample, channels=channels, buffer=buffer_size)
        pygame.mixer.set_num_channels(20)

        # Tone Generation
        self.initial_frequency = int(initial_freq)
        self.final_frequency = int(final_freq)
        self.frequency_range = int(self.final_frequency-self.initial_frequency+1)
        self.array = ["" for i in range(self.frequency_range)]
        self.generate_all_tones()

# --------------------------------------------------

    def generate_all_tones(self):
        """Function that creates all the tones that might be used"""
        # Tone Generation
        for j in range(self.frequency_range):
            arr = numpy.array([4096 * numpy.sin(2.0 * numpy.pi * (self.initial_frequency+j) * t / 44100) for t in range(0, int(441+DATA.DISPLACEMENTS_441[int(self.initial_frequency+j-120)]))]).astype(numpy.int16)
            arr2 = numpy.c_[arr, arr]
            sound_mixer = pygame.mixer.Sound(arr2)
            self.array[j] = sound_mixer

# --------------------------------------------------

    def one_stop(self):
        """Function that stops playing one tone"""
        self.one_lower_volume(0.0)
        pygame.mixer.Channel(0).stop()

# --------------------------------------------------

    def one_set_permanent_volume(self):
        """Function that sets the volume to maximum of a determined tone"""
        pygame.mixer.Channel(0).set_volume(1.0)

# --------------------------------------------------

    def one_set_volume(self, desired_volume):
        """Function that sets the volume of a determined tone"""
        pygame.mixer.Channel(0).set_volume(desired_volume)

# --------------------------------------------------

    def one_rise_volume(self, desired_volume):
        """Function that makes smooth upward volume transitions"""
        current_volume = pygame.mixer.Channel(0).get_volume()
        time_sleep = -self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Channel(0).set_volume(j/100)
            time.sleep(time_sleep)
        pygame.mixer.Channel(0).set_volume(desired_volume)

# --------------------------------------------------

    def one_lower_volume(self, desired_volume):
        """Function that makes smooth downward volume transitions"""
        current_volume = pygame.mixer.Channel(0).get_volume()
        time_sleep = self.max_time/(int(current_volume*100)-int(desired_volume*100))
        step = int(round((self.max_time*1000)/(int(current_volume*100)-int(desired_volume*100))))
        for j in range(int(current_volume*100), int(desired_volume*100), -step):
            pygame.mixer.Channel(0).set_volume(j/100)
            time.sleep(time_sleep)
        pygame.mixer.Channel(0).set_volume(desired_volume)

# --------------------------------------------------

    def set_freq(self, desired_freq):
        """Function that sets the frequency of the tone to the one desired"""
        #for j in range(int(self.max_time/self.tone_duration)):
        for j in range(5):
            while pygame.mixer.Channel(0).get_queue() is not None:
                time.sleep(0.001)
            pygame.mixer.Channel(0).queue(self.array[int(desired_freq-120)])
        self.currently_playing = int(desired_freq)

# --------------------------------------------------

    def set_freq_2(self, desired_freq):
        """Function that sets the frequency of the tone to the one desired"""
        pygame.mixer.Channel(0).play(self.array[int(desired_freq-120)], 8)

# --------------------------------------------------

    def one_rise_freq(self, desired_freq):
        """Function that makes smooth upward frequency transitions"""
        step = int(round((self.max_time*1000)/(self.tone_duration*1000)))
        for j in range(self.currently_playing, int(desired_freq), -step):
            while pygame.mixer.Channel(0).get_queue() is not None:
                time.sleep(0.001)
            pygame.mixer.Channel(0).queue(self.array[j-120])
        while pygame.mixer.Channel(0).get_queue() is not None:
            time.sleep(0.001)
        pygame.mixer.Channel(0).queue(self.array[int(desired_freq-120)])
        self.currently_playing = int(desired_freq)

# --------------------------------------------------

    def one_lower_freq(self, desired_freq):
        """Function that makes smooth downward frequency transitions"""
        step = int(round((self.max_time*1000)/(self.tone_duration*1000)))
        for j in range(self.currently_playing, int(desired_freq), -step):
            while pygame.mixer.Channel(0).get_queue() is not None:
                time.sleep(0.001)
            pygame.mixer.Channel(0).queue(self.array[j-120])
        while pygame.mixer.Channel(0).get_queue() is not None:
            time.sleep(0.001)
        pygame.mixer.Channel(0).queue(self.array[int(desired_freq-120)])
        self.currently_playing = int(desired_freq)

# --------------------------------------------------

if __name__ == "__main__":
    sound_tone = Sound_Tone_Full(DATA.C3-20, DATA.C4+40)
    print("Done")
    time.sleep(1)
    while True:
        for i in range(20):
            sound_tone.set_freq(DATA.C3)
        sound_tone.one_rise_freq(DATA.D3)
        sound_tone.one_rise_freq(DATA.E3)
        sound_tone.one_rise_freq(DATA.F3)
        sound_tone.one_rise_freq(DATA.G3)
        sound_tone.one_rise_freq(DATA.A3)
        sound_tone.one_rise_freq(DATA.B3)
        sound_tone.one_rise_freq(DATA.C4)
        for i in range(20):
            sound_tone.set_freq(DATA.C4)
        sound_tone.one_lower_freq(DATA.B3)
        sound_tone.one_lower_freq(DATA.A3)
        sound_tone.one_lower_freq(DATA.G3)
        sound_tone.one_lower_freq(DATA.F3)
        sound_tone.one_lower_freq(DATA.E3)
        sound_tone.one_lower_freq(DATA.D3)
        sound_tone.one_lower_freq(DATA.C3)

# --------------------------------------------------
