"""
shutters.py
Lennard Vanderspek
3/12/2019

/----------------------------------------\
|THIS CODE HAS NOT BEEN TESTED IN ANY WAY|
\----------------------------------------/

This is an update version of an old file temp.py. The api has been improved to
scale across multiple shutters in an organized fashion
"""

import nidaqmx
import time

# default time for shutter wait after sending open signal
DEFAULT_WAIT_TIME = 0.6
#default time to wait to resend open signal after failure
DEFAULT_RETRY     = 1

class Shutter:
    def __init__(self, output_channel, return_channel, task_name):
        self.task = nidaqmx.Task(new_task_name=task_name)
        self.task.do_channels.add_do_chan(output_channel)
        self.task.di_channels.add_di_chan(return_channel)

    def __del__(self):
        self.task.close()

    #should theoretically not fail if it is simply cutting power to shutter
    def close(self):
        self.task.write(False) #writing might be strange with multiple channels

    #will send the signal to open shutter, might fail
    def try_open(self):
        self.task.write(True) #writing might be strange with multiple channels

    #repeatedly tries to open shutter until successful
    def open(self, wait_time=DEFAULT_WAIT_TIME, retry_period=DEFAULT_RETRY):
        while True:
            self.try_open()
            time.sleep(wait_time)
            if task.read(): break
            self.close()
            time.sleep(retry_period)


#sample usage
"""
shutter1 = Shutter(
    output_channel='Dev1/port0/line0', 
    return_channel='Dev1/port0/line1',
    task_name='shutter1',
)
shutter1.open() #will try to repeatedly try to open using default values
time.sleep(1)
shutter1.close()
shutter1.try_open() #will probably fail because capacitors will not be charged
"""
