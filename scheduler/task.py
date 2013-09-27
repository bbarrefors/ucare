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
from bjornAPI import set_freq, get_cpu_util

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

def l2394(loops):
    """
    _loop_

    
    """
    set_freq(2394000)
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 18500):
                k += 1


if __name__ == '__main__':
    #print(get_cpu_util())
    t = timeit.Timer("l1463(200)", setup="from __main__ import l1463")
    print t.timeit(number=1)
    #l1463(10)
