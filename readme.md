#Micropython Flashy Clock
This changes color based on the minutes from 0-59 every hour. Every 15 minutes it does a subtle flash. 

##Quickstart 
Put your free key from https://timezonedb.com/ into the `key` variable in config.py. Then upload all these files and open up a webrepl and type `main_loop()`

##Example sped up:

![image of project with light on wall](https://media.giphy.com/media/tPRepiQ9dNGKc/giphy.gif)

##Guide
Using an adafruit feather esp8266 and a NeoPixel board you can use color to always know roughly what time it is. I put this behind my monitor. 

To upload the code, start a micropython repl by going here:

http://micropython.org/webrepl/?

And put in your ip address which you can get from connecting to the board via serial through putty and getting the output of webrepl.start(), or you can just try a few ips on your network till it works. Mine was 192.168.0.**108** so just try 101-115 

If there are questions about that step then follow the getting started tutorial here https://learn.adafruit.com/micropython-basics-esp8266-webrepl/access-webrepl

##Parts

Adafruit Feather esp8266: https://www.adafruit.com/product/2821 

Adafruit NeoPixel Featherwing: https://www.adafruit.com/product/2945 
