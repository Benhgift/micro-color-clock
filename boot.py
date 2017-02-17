import sys
import esp                                                                                             
import gc                                                                                               
import webrepl                                                                                          

esp.osdebug(None)                                                                                      
webrepl.start()                                                                                         
gc.collect()


def readfile(file="boot.py"):
    with open(file,'r') as thefile:
        for line in thefile:
            print(line, end='')
    print()


def wipe_module(module):
    del sys.modules[module]


def rel():
    try:
        wipe_module('main')
        wipe_module('test_all')
        wipe_module('pixel')
        wipe_module('timing')
        wipe_module('config')
    except:
        pass
    from main import *
    from test_all import *
