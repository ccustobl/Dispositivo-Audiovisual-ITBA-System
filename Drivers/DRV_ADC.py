# --------------------------------------------------

"""Driver for Analog-Digital Converter"""
# Author: Custo Blanch, Christian
# ITBA

# --------------------------------------------------

# Imports
import Adafruit_ADS1x15 as ADS

# --------------------------------------------------

class ADC():
    """Sound reproduction functions"""

# --------------------------------------------------

    def  __init__(self, address):
        """Initialization"""
        # Variable initialization
        self.gain = 1 # 1 = +/-4.096V ; selected because RPi works with 3.3V

        # ADC initialization
        self.ad_conv = ADS.ADS1115(address)

# --------------------------------------------------

    def adc_read(self, channel):
        """Function that gets a single value from the ADC"""
        value = self.ad_conv.read_adc(channel, gain=self.gain)

        return value

# --------------------------------------------------

    def adc_start_cont(self, channel, high_thresh, low_thresh):
        """Function that starts continuous conversion mode in the ADC, it will pull high the alert when a meassurement is between the thresholds and it will be held until the value is read"""
        self.ad_conv.start_adc_comparator(channel, high_thresh, low_thresh, active_low=False, traditional=True, latching=True, num_readings=1, gain=self.gain)
        # active_low: True = Alert is pulled low when triggered
        # traditional: True = Alert fires when between high_thresh and low_thresh
        # latching: True = Alert is held until get_last_result() is called to read the value

# --------------------------------------------------

    def adc_get_value(self):
        """Function that retrieves the last conversion made by the ADC"""
        value = self.ad_conv.get_last_result()

        return value

# --------------------------------------------------

    def adc_stop(self):
        """Function that stops all continuous conversions in the ADC"""
        self.ad_conv.stop_adc()

# --------------------------------------------------
