# -*- coding: utf-8 -*-

"""Base set of pigo commands you can import into your root namespace"""

import stackless

from time import time

schedule = stackless.schedule
tasklet = stackless.tasklet

def sleep(tick=1):
    """
    Sleep the tasklets for the given number of frames. Defaults to one frame
    """
    for frame in range(tick):
        schedule(None)

def sleep_until(until):
    """Sleep until the requested time (in epoch seconds) comes up. May actually sleep longer than intended.
    If time is in the past, returns immediately.
    """
    if until<time():
        # time has already past
        return
        
    while time.time()<until:
        schedule(None)

def delay(seconds):
    """Sleep the tasklet for this many seconds"""
    return sleep_until( time()+seconds )
        

        
        