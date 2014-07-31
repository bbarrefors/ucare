#!/usr/bin/python26 -B
"""
_simulator_

Created by Bjorn Barrefors on 26/9/2013

University of Nebraska-Lincoln
"""
###############################################################################
#                                                                             #
#                             S I M U L A T O R                               #
#                                                                             #
###############################################################################

import sys
import time
from multiprocessing import Process

from task import task
################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################

def main(node):
    """
    __main__


    """
    numTasks = [250, 350, 450]
    totUtils = [25, 35, 45]
    algs = ['HyMWGA', 'BaB']

    files = []

    for u in totUtils:
        for t in numTasks:
            for a in algs:
                files.append('/home/tarek/bjorn/bjorn/simulation/u%dt%da%s' % (u, t, a))
                
    fd = open('/home/tarek/bjorn/bjorn/simulation/Schedule', 'r')
    lines = fd.readlines()
    j = 0
    for line in lines:
        l = line.partition("\t")
        cpu = l[0]
        if cpu == str(node):
            if l[2] == 0:
                p = 0
            else:
                u = float(l[2])
                u = u/4
                time_e = 10*u
                loops = time_e * 100
                process = Process(target=task, args=(loops, u, files[j]))
                process.start()
                process.join()
                time.sleep(300)
            j += 1
    fd.close()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
