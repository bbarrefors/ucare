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

#from task import task

################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################

def main():
    """
    __main__

    
    """
    tasks = [100, 150, 200, 300]
    util = [20, 35, 45]
    pop = [2000, 10000]
    alg = ['G', 'WF', 'HWG']
    file_names = []
    for task in tasks:
        for u in util:
            for p in pop:
                for a in alg:
                    file_names.append('t%du%dp%da%s' % (task, u, p, a))

    fs = open('Schedule', 'r')
    lines = fs.readlines()
    j = 0
    i = 1
    for line in lines:
        l = line.partition("\t")
        cpu = l[0]
        if cpu == str(i):
            u = float(l[2])
            u = u/4
            time = 10*u
            loops = time * 100
            process = Process(target=task, args=(loops, u, file_names[j]))
            process.start()
            process.join()
            j += 1
    fs.close()
    print j
    return 0

if __name__ == '__main__':
    sys.exit(main())
