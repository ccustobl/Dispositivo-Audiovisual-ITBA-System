# --------------------------------------------------

"""Variables that affect the functioning of APP"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# PINs in use
PIN_SENSOR = [4, 14, 15] # 14 15 # Mux0, Mux1, Mux2
PIN_UI = [0, 0]
PIN_LED = [17, 27, 22] #R, G, B
PIN_D_M_ENABLE = [26, 19, 13] # E3, E2, E1
PIN_D_M_ADDRESS = [16, 20, 21] # A2, A1, A0
PIN_SHUTDOWN = 18
PIN_SDA = 2
PIN_SCL = 3
PIN_ADC_ALERT = 800 # Not in use
PIN_KY038_DIG = 25
PIN_KY038_ANL = 800 # Not in use
PIN_SWITCH = [11, 9, 10] # S0, S1, S2

# --------------------------------------------------

# HC-SR04 parameters
MAXIMUM_DISTANCE = 500 # maximum distance in mm (using a high maximum distance will add noise)
SAMPLE_NUMBER = 1 # number of samples used in averaging (each sample is taken every 60ms) (using multiple samples will improve accuracy, but will lower responsiveness)
HCSR04_INTERRUPTIONS = False
RPI_TRIGGER = False

# --------------------------------------------------

# KY038 parameters
CLAP_INTERRUPTIONS = True

# --------------------------------------------------

# LED parameters
LED_FREQ = 1000 # PWM frequency in Hz (if using Software PWM, FREQ cant be higher than 100HZ)
PWM_SW_SELECT = True

# --------------------------------------------------

# ADC parameters
ADDRESS_1 = 0x48 # GND (in use)
ADDRESS_2 = 0x49 # VDD
ADDRESS_3 = 0x4A #
ADDRESS_4 = 0x4B #
# Piezo ADC Value: 3.3V = 23350, GND = -850
HIGH_THRESH = 300000 # Piezo ADC Value
LOW_THRESH = 1000 # Piezo ADC Value

# --------------------------------------------------

# Potetiometer
# Pots give 10 full turns
POT_R = 0
POT_G = 1
POT_B = 2
POT_W = 3
POTS = [POT_R, POT_G, POT_B, POT_W]
POT_MAX_VALUE = 26320 # Maximum meassured = 26334, 3.3V = 26343
POT_MIN_VALUE = 50 # Minimun meassured = 36

# --------------------------------------------------
