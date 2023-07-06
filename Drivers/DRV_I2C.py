# --------------------------------------------------

"""Driver for I2C"""
# Author: Custo Blanch, Christian
# ITBA

# --------------------------------------------------

# Imports
import re
import subprocess
import Drivers.DRV_SMBUS as smbus

# --------------------------------------------------

def get_i2c_default_bus():
    """ Function that returns the default bus number"""

    with open('/proc/cpuinfo', 'r') as infile:
        for line in infile:
            # Match a line of the form Revision
            match = re.match('Revision\s+:\s+.*(\w{4})$', line, flags=re.IGNORECASE)
            if match and match.group(1) in ['0000', '0002', '0003']:
                # Return Port 0 if Revision 1 (if revision ends with 0000, 0002 or 0003)
                return 1
            elif match:
                # Return Pot 1 if Revision 2 (if revision ends with any other 4 chars)
                return 2
            else:
                raise RuntimeError('Could not determine default I2C bus for platform.')

# --------------------------------------------------

def require_repeated_start():
    """"Enable repeated start conditions for I2C register reads"""

    subprocess.check_call('chmod 666 /sys/module/i2c_bcm2708/parameters/combined', shell=True)
    subprocess.check_call('echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined', shell=True)

# --------------------------------------------------

class I2C_Device(object):

    def __init__(self, address, busnum):
        """Create an instance of the I2C device at the specified address on the specified I2C bus number"""
        self._address = address
        self._bus = smbus.SMBus(busnum)

    def write_list(self, register, data):
        """Write bytes to the specified register."""
        self._bus.write_i2c_block_data(self._address, register, data)

    def read_list(self, register, length):
        """Read a length number of bytes from the specified register. Results will be returned as a bytearray."""
        results = self._bus.read_i2c_block_data(self._address, register, length)
        return results

# --------------------------------------------------
