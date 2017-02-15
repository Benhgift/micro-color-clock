import time
import urequests
from time import sleep


class Timing:
    def __init__(self, url, secs_between_flashes, pixels):
        self.url = url
        self.secs_between_flashes = secs_between_flashes
        self.pixels = pixels
        self.last_flash = None
        self._secs_in_an_hour = 60 * 60
        self._secs_till_update = 11
        self.min_time_between_flashes = 10
        self._update()

    def _update_if_needed(self):
        if  (time.time() - self.last_update) > self._secs_till_update:
            self._update()

    def _update(self):
        start = time.time()
        print("updating")
        try:
            real_time = self.get_time_online(self.url)
            self.secs_into_hour = real_time['m'] * 60 + real_time['s']
            self.hour_zero = start - self.secs_into_hour
            self.last_update = time.time()
        except:
            print("error, test your timezonedb key")
            sleep(2)
            self._update()

    def get_secs_into_hour(self):
        self._update_if_needed()
        time_since_zero = time.time() - self.hour_zero 
        return time_since_zero % self._secs_in_an_hour

    def _check_if_time_to_flash(self):
        if self.last_flash:
            time_since_flash = time.time() - self.last_flash
            if time_since_flash < self.min_time_between_flashes:
                return False
        secs_into_hour = self.get_secs_into_hour()
        if secs_into_hour % self.secs_between_flashes < 3:
            return True
        return False

    def flash_if_its_time_to(self, color):
        if not self._check_if_time_to_flash():
            return False
        def color_func():
            self.pixels.brightness([int(x * 2.2) for x in color])
        self._flash(color_func)
        self.last_flash = time.time()
        return True

    @staticmethod
    def _flash(color_func):
        color_func()
        sleep(1)

    @staticmethod
    def get_time_online(url):
        response = urequests.get(url)
        time = response.json()['formatted'].split()[1]
        time = [int(x) for x in time.split(':')]
        return {'h':time[0], 'm':time[1], 's':time[2]}



