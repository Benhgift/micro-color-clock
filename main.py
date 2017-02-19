import time
import sys
import urequests
import config
import hls
from pixel import Pixels
from timing import Timing
from time import sleep


def get_percent_of_hour(seconds_passed):
    return (seconds_passed / (60 * 60))


def get_color(seconds_passed):
    percent = get_percent_of_hour(seconds_passed)
    # start at green
    adjusted_percent = hls.ONE_THIRD + percent
    max_brightness = 100
    # hls will double the brightness so we cut it in half first
    hls_brightness = max_brightness/2
    rgb = hls.hls_to_rgb(adjusted_percent, hls_brightness, -1.007905138339921)
    return [int(x) for x in rgb]


def record_error(exc):
    with open('last_error', 'w') as f:
        sys.print_exception(exc, f)
    with open('last_error', 'a+') as f:
        _time = time.time()
        f.write('\n\n' + str(_time) + '\n')
        sleep(10)


def main_loop():
    print("starting loop")
    pixels = Pixels()
    timing = Timing(config.url, config.secs_between_flashes, pixels)
    while True:
        sleep(1)
        try:
            seconds_passed = timing.get_secs_into_hour()
            color = get_color(seconds_passed)
            if seconds_passed % 5 == 0:
                print(color)
            timing.flash_if_its_time_to(color)
            pixels.brightness(color)
        except Exception as e:
            print("error")
            record_error(e)
