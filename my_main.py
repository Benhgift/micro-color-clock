import time
import urequests
import config
from neopixel import NeoPixel
from machine import Pin
from time import sleep


PXL_NUM = 32
PXL_WID = 8
PXL_HIG = 4
p = NeoPixel(Pin(15), 32)

blue = lambda: brightness(p, (0, 0, 110))
red = lambda: brightness(p, (110, 0, 0))
green = lambda: brightness(p, (0, 110, 0))
black = lambda: brightness(p, (0, 0, 0))
white = lambda: brightness(p, (110, 110, 110))


# NeoPixel helper functions -------


def brightness(px=NeoPixel(Pin(15), 32), val=(2,2,2)):
    for y in range(PXL_NUM):
        px[y] = val
    px.write()


def set_col(px, val, col):
    for x in range(PXL_HIG):
        px[col] = val
        col += PXL_WID 
    px.write()


def scroll(px, val, direction = 'forward'):
    cols = range(PXL_WID) if direction == 'forward' else reversed(range(PXL_WID))
    for x in cols:
        brightness(px, (0, 0, 0))
        set_col(px, val, x)
        sleep(.03)


def neato_scroll(px):
    x = 0
    while True:
        x = ((x + 1) % 20) + 1
        y = x if x%2 else 0
        z = x if x%3 else 0
        scroll(px, (x, y, z))
        scroll(px, (x, y, z), 'r')


# Time data -----

url = 'http://api.timezonedb.com/v2/get-time-zone?key='
url = url + config.key
url = url + '&format=json&by=zone&zone=America/Los_Angeles'

mins_between_flashes = 15
secs_between_flashes = mins_between_flashes * 60


class Timing:
    def __init__(self, url):
        self.update()
        self._secs_in_an_hour = 60 * 60
        self._update_freq = 11

    def seconds_from_last_hour(self):
        self._update_if_needed()
        time_since_zero = time.time() - self.hour_zero 
        return time_since_zero % self._secs_in_an_hour

    def _update_if_needed(self):
        if  (time.time() - self.last_update) > self._update_freq:
            self.update()

    def update(self):
        start = time.time()
        print("updating")
        try:
            real_time = get_time_online(url)
            secs_from_hour = real_time['m'] * 60 + real_time['s']
            self.hour_zero = start - secs_from_hour
            self.last_update = time.time()
        except:
            print("error")
            sleep(2)
            self.update()


def get_time_online(url):
    response = urequests.get(url)
    time = response.json()['formatted'].split()[1]
    time = [int(x) for x in time.split(':')]
    return {'h':time[0], 'm':time[1], 's':time[2]}


def flash_if_its_time_to(seconds_passed, color):
    if not (seconds_passed % secs_between_flashes) < 3:
        return
    color_func = lambda: brightness(p, [x * 2 for x in color])
    _flash(color_func)


def _flash(color_func):
    color_func()
    sleep(2)


def get_percent_of_hour(seconds_passed):
    if seconds_passed == 0:
        return 0
    return seconds_passed / (60 * 60)


def get_color(seconds_passed):
    percent = get_percent_of_hour(seconds_passed) * 100
    max_brightness = 50
    scale = 3 * (max_brightness / 100)
    if percent < 33.3334:
        blue = percent * scale
        green = (33.333 - percent) * scale
        return [0, int(green), int(blue)]
    if percent < 66.6667:
        red = (percent - 33.333) * scale
        blue = (66.666 - percent) * scale
        return [int(red), 0, int(blue)]
    else:
        green = (percent - 66.666) * scale
        red = (100 - percent) * scale
        return [int(red), int(green), 0]
    


def main_loop():
    print("starting loop")
    timing = Timing(url)
    while True:
        sleep(1)
        seconds_passed = timing.seconds_from_last_hour()
        color = get_color(seconds_passed)
        flash_if_its_time_to(seconds_passed, color)
        brightness(p, color)


def test_loop():
    print("starting loop")
    timing = Timing(url)
    seconds_passed = 0
    while True:
        sleep(1)
        print("mins passed = " + str(seconds_passed/60))
        if seconds_passed > (60*60):
            seconds_passed = 0
        #seconds_passed = timing.seconds_from_last_hour()
        color = get_color(seconds_passed)
        flash_if_its_time_to(seconds_passed, color)
        brightness(p, color)
        seconds_passed += 60
