import time
from neopixel import NeoPixel
from machine import Pin
from time import sleep


class Pixels:
    def __init__(self, width=8, hight=4, pin=15):
        self.PXL_WID = width
        self.PXL_HIG = hight
        self.PXL_NUM = width * hight
        # pin 15 needs solder. See adafruit featherwing tutorial
        self.px = NeoPixel(Pin(15), self.PXL_NUM)  

        self.blue = lambda: self.brightness((0, 0, 110))
        self.red = lambda: self.brightness((110, 0, 0))
        self.green = lambda: self.brightness((0, 110, 0))
        self.black = lambda: self.brightness((0, 0, 0))
        self.white = lambda: self.brightness((110, 110, 110))

    def brightness(self, val=(0,0,0)):
        for y in range(self.PXL_NUM):
            self.px[y] = val
        self.px.write()

