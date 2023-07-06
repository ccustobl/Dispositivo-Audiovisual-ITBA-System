# --------------------------------------------------

"""Variables needed to use MIDIs"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Musical Notes
C = 0
C_S = 1
D = 2
D_S = 3
E = 4
F = 5
F_S = 6
G = 7
G_S = 8
A = 9
A_S = 10
B = 11

C0 = 12
C0_S = 13
D0 = 14
D0_S = 15
E0 = 16
F0 = 17
F0_S = 18
G0 = 19
G0_S = 20
A0 = 21
A0_S = 22
B0 = 23

C1 = 24
C1_S = 25
D1 = 26
D1_S = 27
E1 = 28
F1 = 29
F1_S = 30
G1 = 31
G1_S = 32
A1 = 33
A1_S = 34
B1 = 35

C2 = 36
C2_S = 37
D2 = 38
D2_S = 39
E2 = 40
F2 = 41
F2_S = 42
G2 = 43
G2_S = 44
A2 = 45
A2_S = 46
B2 = 47

C3 = 48
C3_S = 49
D3 = 50
D3_S = 51
E3 = 52
F3 = 53
F3_S = 54
G3 = 55
G3_S = 56
A3 = 57
A3_S = 58
B3 = 59

C4 = 60
C4_S = 61
D4 = 62
D4_S = 63
E4 = 64
F4 = 65
F4_S = 66
G4 = 67
G4_S = 68
A4 = 69
A4_S = 70
B4 = 71

C5 = 72
C5_S = 73
D5 = 74
D5_S = 75
E5 = 76
F5 = 77
F5_S = 78
G5 = 79
G5_S = 80
A5 = 81
A5_S = 82
B5 = 83

C6 = 84
C6_S = 85
D6 = 86
D6_S = 87
E6 = 88
F6 = 89
F6_S = 90
G6 = 91
G6_S = 92
A6 = 93
A6_S = 94
B6 = 95

C7 = 96
C7_S = 97
D7 = 98
D7_S = 99
E7 = 100
F7 = 101
F7_S = 102
G7 = 103
G7_S = 104
A7 = 105
A7_S = 106
B7 = 107

C8 = 108
C8_S = 109
D8 = 110
D8_S = 111
E8 = 112
F8 = 113
F8_S = 114
G8 = 115
G8_S = 116
A8 = 117
A8_S = 118
B8 = 119

C9 = 120
C9_S = 121
D9 = 122
D9_S = 123
E9 = 124
F9 = 125
F9_S = 126
G9 = 127
G9_S = 128
A9 = 129
A9_S = 130
B9 = 131

# --------------------------------------------------

# Chords
MAJOR_CHORD = [0, 4, 7]
MINOR_CHORD = [0, 3, 7]

# Arpeggios
MAJOR_ARP = [0, 4, 7, 12]
MINOR_ARP = [0, 3, 7, 12]

# Scales
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11, 12]
MAJOR_SCALE_EXT = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10, 12]
MINOR_SCALE_EXT = [0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24]

# --------------------------------------------------

# Instruments
PIANO_BASIC = 0 #S
PIANO_BASIC_2 = 1 #S
PIANO_BASIC_3 = 2 #S
PIANO_BASIC_3 = 3 #S
PIANO_MUTE = 4 #M
PIANO_SOFT =5 #M
PIANO_BRIGHT = 6 #S
XYLOPHONE_BASIC = 8 #S
BELL = 9 #S
XYLOPHONE_BRIGHT = 10 #M
XYLOPHONE_2 = 11 #S
XYLOPHONE_OPAQUE = 12 #S
BELL_WOOD = 13 #S
BELL_METAL = 14 #S
ORGAN_BASIC = 16 #C
ORGAN_2 = 17 #C
#C up to 23
GUITAR_BASIC = 24 #S
GUITAR_BRIGHT = 25 #M
GUITAR_MUTED = 28 #vs
GUITAR_ELECTRIC = 29 #M
GUITAR_ELECTRIC_2 = 30 #C
GUITAR_ELECTRIC_2 = 31 #C
KEYBOARD_SPACE_1 = 35 #M
KEYBOARD_8BIT = 38 #C
VIOLIN_BASIC = 40 #C
VIOLIN_2 = 41 #C
VIOLIN_3 = 42 #C
VIOLIN_4 = 43 #C
VIOLIN_5 = 44 #C
VIOLIN_6 = 45 #S
HARP_BASIC = 46 #S
CHOIR_BASIC = 52 #C
CHAN = 55 #S
TRUMPET_BASIC = 56 #C
DISNEY_1 = 68 #C
DISNEY_VIOLIN = 69 #C
FLUTE_BASIC = 71 #C
FLUTE_TRIBE = 72 #C
FLUTE_MOUNTAINS = 75 #C
KEYBOARD_SPACE_2 = 78 #C #UFO
ENYA = 82 #C # Piano with echo
KEYBOARD_8BIT_ECHO = 86 #C
PIANO_SOFT = 88 #L
PIANO_SLEEP = 90 #C
PIANO_CARTOON = 96 #C
PIANO_EPIC = 97 #C
PIANO_8BIT = 98 #S
PIANO_ECHO = 99 #M
GUITAR_ASIAN = 104 #M
GUITAR_4 = 105 #M
SHAMISEN = 106 #M
GUITAR_5 = 107 #S
STICKS = 108 #S
POTS = 112 #S
POTS_2 = 113 #S #HIGH PITCH
HANG_DRUM = 114 #S
COWBELL = 115 #S
DRUM = 116 #S
TOM = 117 #S
TOM_2 = 118 #S
CYMBAL = 119 #S
STRING = 120 #S
EXHALE = 121 #S
CLAP_WAVE = 122 #S
BIRD = 123 #S
PHONE = 124 #S
CHOPPER = 125 #L
RAIN = 126 #L

# Instruments
INSTRUMENTS = [0, 8, 116]

# Continuous
CONTINUOUS = []
CONTINUOUS_ALL = [18, 19, 20, 38, 39, 43, 46, 50, 56, 60, 71, 85, 86, 87, 94]

# --------------------------------------------------
