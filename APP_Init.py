# --------------------------------------------------

"""App that controls the Overhead Projector"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports

import time
import threading
import multiprocessing as mp
from Ultrasonic import Ultrasonic
from Sound_Music import Music
from LED_Light import Light
from Shutdown import Shutdown

# --------------------------------------------------

def APP_main():
    """Main Loop of the Overhead Projector"""
  
    # Light Initialization
    light = Light()
    light_process = mp.Process(target=light.light_main, args=())
    light_process.start()
    time.sleep(0.1)

    # Music Reproduction Initialization
    music = Music()
    music_thread = threading.Thread(target=music.main_final, args=())
    music_thread.start()
    time.sleep(0.1)

    # Ultrasonic Sensors Initialization
    ultra = Ultrasonic()
    #ultra_process = mp.Process(target=ultra.ultrasonic_main_loop_filter_3, args=())
    ultra_process = mp.Process(target=ultra.ultrasonic_main_filter_4, args=())
    ultra_process.start()
    time.sleep(0.1)
    
    # Shutdown Initialization
    shutdown = Shutdown()
    shutdown.shutdown_main()
    time.sleep(1)

    print('Ready')

    # Main Loop
    #while True:
    #    time.sleep(86400)

# --------------------------------------------------

if __name__ == "__main__":
    APP_main()

# --------------------------------------------------
