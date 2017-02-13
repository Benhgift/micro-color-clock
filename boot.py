import sys
import esp                                                                                             
import gc                                                                                               
import webrepl                                                                                          
from my_main import *
import my_main 

esp.osdebug(None)                                                                                      
webrepl.start()                                                                                         
gc.collect()


def readfile(file="boot.py"):
  with open(file,'r') as thefile:
      data = thefile.read()
  print(data)


def wipe_module(module):
    del sys.modules[module]


def rel():
    try:
        wipe_module('my_main')
    except:
        pass
    from my_main import *
    import my_main
