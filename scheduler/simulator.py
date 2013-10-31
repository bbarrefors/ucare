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
from time import sleep
from multiprocessing import Process

from task import task

################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################

def main():
    """
    __main__
    
    
    """
    file_names = ['output/t100u20p10000aG', 'output/t100u20p10000aWF', 'output/t100u20p10000aHWG', 'output/t150u35p10000aG',
                  'output/t150u35p10000aWF', 'output/t150u35p10000aHWG', 'output/t200u45p10000aG', 'output/t200u45p10000aWF',
                  'output/t200u45p10000aHWG', 'output/t300u45p10000aG', 'output/t300u45p10000aWF', 'output/t300u45p10000aHWG']
    
    fd = open('Schedule', 'r')
    lines = fd.readlines()
    j = 0
    i = 20
    for line in lines:
        l = line.partition("\t")
        cpu = l[0]
        if cpu == str(i):
            sleep(60)
            if l[2] == 0:
                u = 0
                loops = 0
            else:
                u = float(l[2])
                u = u/4
                time = 10*u
                loops = time * 100
            process = Process(target=task, args=(loops, u, file_names[j]))
            process.start()
            process.join()
            j += 1
    fd.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
