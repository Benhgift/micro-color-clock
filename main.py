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
    # this maps color to each position of the list that NeoPixel expects
    color_map = {'r':0, 'g':1, 'b':2}
    # this maps color onto the positions of the HOUR. Right now it's in thirds
    # but {0:green, 1:red} would mean "be green for the first half hour, then red"
    split_map = {0:color_map['g'], 1:color_map['b'], 2:color_map['r']}
    # how many segments have we split the hour into
    splits = len(split_map)
    # a chunk is one segment of the hour out of 100%. Note the float bugfix
    chunk = 100.0001 / splits  
    scale = (splits/100) * max_brightness
    for i in range(1, splits+1):
        cur_chunk = chunk * i
        last_chunk = chunk * (i-1)
        if percent <= cur_chunk:
            vals = [0] * len(color_map)
            growing_color = (percent - last_chunk) * scale
            shrinking_color = (cur_chunk - percent) * scale
            vals[split_map[i-1]] = shrinking_color
            vals[split_map[(i) % splits]] = growing_color
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
