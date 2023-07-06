# --------------------------------------------------

"""Driver to control WAV reproduction"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import time
import pygame

# --------------------------------------------------

class Sound_WAV():
    """Sound reproduction functions"""

# --------------------------------------------------

    def  __init__(self):
        """Initialization"""

        # Variable initialization
        pygame.mixer.init(44100, -16, 1, 1024)

        # WAVs Loading3#
        self.wav_lib = [pygame.mixer.Sound('/home/pi/WAVs/deepbark.wav'), # Domestic Animals
                        pygame.mixer.Sound('/home/pi/WAVs/cat.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/cow.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/pig.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/horse.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/donkey.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/sheep.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/rooster.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/chicken.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/duck.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/birds2.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/goat.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/turkey.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/crickets.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/rain.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/lion2.wav'), # Wild Animals
                        pygame.mixer.Sound('/home/pi/WAVs/hippo.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/elephant.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/zebra.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/monkey.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/rattlesnake.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/panther.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/wolf.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/crow.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/grizzbear.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/whale.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/penguin.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/wind.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/ocean_edge.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/rainforest.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Kick0.wav'), # Drumkit
                        pygame.mixer.Sound('/home/pi/WAVs/Kick1.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Tom0.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Tom1.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Tom2.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Snare1.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Snare2.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Crash0.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Crash1.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Ride1.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Ride2.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Gong.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/Cowbell.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/HiHat1.wav'),
                        pygame.mixer.Sound('/home/pi/WAVs/HiHat2.wav')] 

        self.set_vol(0.16)
        for counter in range(30,len(self.wav_lib),1):
            self.set_vol_specific(counter, 0.21)

# --------------------------------------------------

    def play_wav(self, number):
        """Function that starts the reproduction of a WAV file"""
        pygame.mixer.Sound.play(self.wav_lib[number])

# --------------------------------------------------

    def stop_wav(self, number):
        """Function that stops the reproduction of a WAV file"""
        pygame.mixer.Sound.stop(self.wav_lib[number])

# --------------------------------------------------

    def set_vol(self, value):
        """Function that sets the volume of all WAV files"""
        for counter in range(len(self.wav_lib)):
            pygame.mixer.Sound.set_volume(self.wav_lib[counter], value)

# --------------------------------------------------

    def set_vol_specific(self, pos, value):
        """Function that sets the volume of all WAV files"""
        pygame.mixer.Sound.set_volume(self.wav_lib[pos], value)

# --------------------------------------------------

    def get_len(self, number):
        """Function that sets the volume of all WAV files"""
        length = pygame.mixer.Sound.get_length(self.wav_lib[number])
        return length

# --------------------------------------------------

    def test(self):
        pygame.mixer.Sound.play(pygame.mixer.Sound('/home/pi/WAVs/deepbark.wav'))

# --------------------------------------------------

if __name__ == "__main__":
    sound_wav = Sound_WAV()
    while True:
        sound_wav.play_wav(2)
        #sound_wav.test()
        time.sleep(1)

# --------------------------------------------------
