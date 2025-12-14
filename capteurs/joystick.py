import math
import sys
import time
from grove.adc import ADC


class GroveThumbJoystick:

    def __init__(self, channelX, channelY):
        self.channelX = channelX
        self.channelY = channelY
        self.adc = ADC()

    @property
    def value(self):
        return self.adc.read(self.channelX), self.adc.read(self.channelY)

Grove = GroveThumbJoystick


def jsDirection():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = 0 # A0

    sensor = GroveThumbJoystick(int(pin), int(pin + 1))

    x, y = sensor.value
    direction = []
    if x > 600:
        direction.append('right')
    if x < 400:
        direction.append('left')
    if y > 600:
        direction.append('up')
    if y < 400:
        direction.append('down')
        
    return direction
