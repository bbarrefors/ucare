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
    tasks = [100, 150, 200, 300]
    util = [20, 35, 45]
    alg = ['G', 'MW', 'HWF']

    files = []

    for t in tasks:
        for u in util:
            for a in alg:
                files.append('theoretical/t%du%da%s' % (t, u, a))

    fd = open('Schedule', 'r')
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
                time = 10*u
                loops = time * 100
                process = Process(target=task, args=(loops, u, files[j]))
                process.start()
                process.join()
        j += 1
    fd.close()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
