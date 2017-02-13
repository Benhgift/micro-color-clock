#Micropython Flashy Clock

Quickstart: Put your free key from https://timezonedb.com/ into the `key` variable in config.py. Then upload all these files and open up a webrepl and type `main_loop()`

Using an adafruit feather esp8266 and a NeoPixel board you can make it flash a color at an interval so that you always know what time it is. I put this behind my monitor. 

To upload the code, start a micropython repl by going here:

http://micropython.org/webrepl/?

And put in your ip address which you can get from connecting to the board via serial through putty and getting the output of webrepl.start(), alternatively you can just try a few ips on your network till it works. Mine was 192.168.0.108 

If there are questions just follow the getting started tutorial here https://learn.adafruit.com/micropython-basics-esp8266-webrepl/access-webrepl
