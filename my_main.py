import time
import urequests
import config
from pixel import Pixels
from timing import Timing
from time import sleep


def get_percent_of_hour(seconds_passed):
    return (seconds_passed / (60 * 60)) * 100


def get_color(seconds_passed):
    percent = get_percent_of_hour(seconds_passed)
    max_brightness = 100
    color_map = {'r':0, 'g':1, 'b':2}
    split_map = {0:color_map['g'], 1:color_map['b'], 2:color_map['r']}
    splits = len(split_map)
    # float error fix
    chunk = 100.1 / splits  
    scale = (splits/100) * max_brightness
    for i in range(1, splits+1):
        cur_chunk = chunk * i
        last_chunk = chunk * (i-1)
        if percent <= cur_chunk:
            vals = [0] * len(color_map)
            growing = (percent - last_chunk) * scale
            shrinking = (cur_chunk - percent) * scale
            vals[split_map[i-1]] = shrinking
            vals[split_map[(i) % splits]] = growing
            return [int(x) for x in vals]


def main_loop():
    print("starting loop")
    pixels = Pixels()
    timing = Timing(config.url, config.secs_between_flashes, pixels)
    while True:
        sleep(1)
        seconds_passed = timing.get_secs_into_hour()
        color = get_color(seconds_passed)
        print(color)
        timing.flash_if_its_time_to(color)
        pixels.brightness(color)
