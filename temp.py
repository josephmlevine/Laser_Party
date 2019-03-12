# -*- coding: utf-8 -*-
"""
Spyder Editor

Do not trust this script to work as it is now.
This is a temporary script file. It is not complete.

Timing needs to be tuned, and the structure of the file and the api will most
likely change.
"""

import nidaqmx
import time

#simply drops the power fed to the shutter; shouldn't fail
def shutter_close():
    shutter_close = nidaqmx.Task()
    shutter_close.do_channels.add_do_chan("Dev1/port0/line0")
    shutter_close.write(bool(0))
    shutter_close.close()

#will send the signals to open the shutter but might fail
def try_shutter_open():
    shutter_open = nidaqmx.Task()
    shutter_open.do_channels.add_do_chan('Dev1/port0/line0')
    shutter_open.write(bool(1))
    shutter_open.close()

#tries to open shutter until successful; timing causes it to be on the order
# of miliseconds
def shutter_open(): 
    shutter_open = nidaqmx.Task()
    shutter_open.do_channels.add_do_chan('Dev1/port0/line0')
    is_open = nidaqmx.Task()
    is_open.di_channels.add_di_chan('Dev1/port0/line1')

    while True:
        shutter_open.write(bool(1))
        time.sleep(.06) #need to give it time to settle
        if is_open.read(): break
        shutter_open.write(bool(0))
        time.sleep(1) #potentially not enough time, capacitors need to charge

    shutter_open.close()
    is_open.close()


""" for testing the behavior
shutter_close()
time.sleep(.5)
shutter_open()
while True:
    shutter_close()
    time.sleep(.5)
    shutter_open()
    time.sleep(.5)
"""
    
