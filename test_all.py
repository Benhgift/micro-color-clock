import config
import time
from my_main import *
from timing import Timing
from pixel import Pixels


def timing_injection_for_checking_to_flash():
    if time.time() % 10 == 0:
        return True


def test_loop():
    print("starting loop")
    pixels = Pixels()
    timing = Timing(config.url, 11, pixels)
    timing._check_if_time_to_flash = timing_injection_for_checking_to_flash
    seconds_passed = 0
    while True:
        sleep(.01)
        #print("mins passed = " + str(seconds_passed/60))
        if seconds_passed > (60*60):
            seconds_passed = 0
        #seconds_passed = timing.seconds_from_last_hour()
        color = get_color(seconds_passed)
        #print(color)
        timing.flash_if_its_time_to(color)
        pixels.brightness(color)
        seconds_passed += int(60/3)
