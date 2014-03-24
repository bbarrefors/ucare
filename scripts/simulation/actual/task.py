#!/usr/bin/env python26
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
import datetime
from multiprocessing import Process
from time import sleep

from bjornAPI import set_freq, get_cpu_util, get_power

def measure(file_n):
    p_1 = 0
    power = 0
    while (p_1 < 100):
        sleep(0.5)
        power += int(get_power())
        p_1 += 1
    avg_power = power / p_1
    fs = open(file_n, 'a')
    fs.write("%d\n" % (avg_power,))
    fs.close()
    return 0

def run(loops):
    i = 0
    while (i < loops):
        i += 1
        j = 0
        while (j < 6):
            j += 1
            k = 0
            while (k < 18500):
                k += 1

def period(loops):
    p_2 = 0
    while (p_2 < 5):
        p_r1 = Process(target=run, args=(loops,))
        p_r2 = Process(target=run, args=(loops,))
        p_r3 = Process(target=run, args=(loops,))
        p_r4 = Process(target=run, args=(loops,))
        p_r1.start()
        p_r2.start()
        p_r3.start()
        p_r4.start()
        sleep(10)
        p_r1.join()
        p_r2.join()
        p_r3.join()
        p_r4.join()
        p_2 += 1
    return 0

def task(loops, util, file_name):
    """
    _task_

    
    """
    if util == 0:
        fs = open(file_name, 'a')
        fs.write("%d\n" % (0,))
        fs.close()
        return 0
    freq = [ 1197000, 1330000, 1463000, 1596000, 1729000, 1862000, 1995000, 2128000, 2261000, 2394000 ]
    for f in freq:
        if (f/2394000.0) >= (util):
            set_freq(f)
            break
    p_m = Process(target=measure, args=(file_name,))
    p_p = Process(target=period, args=(loops,))
    p_p.start()
    sleep(26)
    p_m.start()
    p_p.join()
    p_m.join()
    return 0

################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################        

#if __name__ == '__main__':
    #util = 0.5
    #loops = 1000
    #set_freq(1197000)
    #freq = [ 0.50, 0.56, 0.61, 0.67, 0.72, 0.78, 0.83, 0.89, 0.94, 1 ]
    #for f in freq:
    #    if f >= util:
    #        set_freq(f * 2394000)
    #        break
    #t = timeit.Timer("run(%d)" % (loops, ), setup="from __main__ import run")
    #print t.timeit(number=1)
    #p_r1 = Process(target=run, args=(loops,))
    #p_r2 = Process(target=run, args=(loops,))
    #p_r3 = Process(target=run, args=(loops,))
    #p_r4 = Process(target=run, args=(loops,))
    #p_r1.start()
    #p_r2.start()
    #p_r3.start()
    #p_r4.start()
    #sleep(5)
    #print(get_cpu_util())
    #p_r1.join()
    #p_r2.join()
    #p_r3.join()
    #p_r4.join()
    #loop(200)
    #t = timeit.Timer("l1463(200)", setup="from __main__ import l1463")
    #print t.timeit(number=1)
    #l1463(10)
