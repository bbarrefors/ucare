#!/usr/bin/env python
"""
_task_

Created by Bjorn Barrefors on 26/9/2013

University of Nebraska-Lincoln
"""
###############################################################################
#                                                                             #
#                             S I M U L A T O R                               #
#                                                                             #
###############################################################################


import timeit
from multiprocessing import Process
from time import sleep

from bjornAPI import set_freq, get_cpu_util, get_power

################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################
        
def l1197(loops):
    """
    _loop_

    
    """
    set_freq(1197000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 8900):
                k += 1

def l1330(loops):
    """
    _loop_

    
    """
    set_freq(1330000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 10000):
                k += 1

def l1463(loops):
    """
    _loop_

    
    """
    set_freq(1463000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 10900):
                k += 1

def l1596(loops):
    """
    _loop_

    
    """
    set_freq(1596000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 11900):
                k += 1

def l1729(loops):
    """
    _loop_

    
    """
    set_freq(1729000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 12900):
                k += 1

def l1862(loops):
    """
    _loop_

    
    """
    set_freq(1862000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 13900):
                k += 1

def l1995(loops):
    """
    _loop_

    
    """
    set_freq(1995000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 14900):
                k += 1

def l2128(loops):
    """
    _loop_

    
    """
    set_freq(2128000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 16900):
                k += 1

def l2261(loops):
    """
    _loop_

    
    """
    set_freq(2261000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 17500):
                k += 1

def measure():
    p = 0
    power = 0
    while (p <= 200):
        sleep(0.5)
        power += int(get_power())
        p += 1
    avg_power = power / p
    fs = open('sim', 'a')
    fs.write("%d\n" % (avg_power,))
    fs.close()
    return 0

def loop(loops):
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 18500):
                k += 1
    return 0

def task(loops):
    """
    _loop_

    
    """
    set_freq(2394000)
    p1 = Process(target=measure, args=())
    p1.start()
    sleep(25)
    p = 0
    while (p <= 10):
        p2 = Process(target=loop, args=(loops,))
        p2.start()
        sleep(10)
        p2.join()
        p += 1
    p1.join()

if __name__ == '__main__':
    #print(get_cpu_util())
    #t = timeit.Timer("l1463(200)", setup="from __main__ import l1463")
    #print t.timeit(number=1)
    #l1463(10)
