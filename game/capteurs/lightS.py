import time ,sys, math
from grove.adc import ADC

__all__ = ["GroveLightSensor"]

class GroveLightSensor(object):
    '''
    Grove Light Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def light(self):
        '''
        Get the light strength value, maximum value is 100.0%

        Returns:
            (int): ratio, 0(0.0%) - 1000(100.0%)
        '''
        value = self.adc.read(self.channel)
        return value

Grove = GroveLightSensor


def lightSensor():
    #from grove.helper import SlotHelper
    #sh = SlotHelper(SlotHelper.ADC)
    pin = 4

    sensor = GroveLightSensor(pin)
    
    return sensor.light


'''while True:
    print(main())
    time.sleep(0.5)
'''
