#!/usr/bin/env python
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

from subprocess import call

################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################

def main():
    """
    __main__

    
    """
    fs = open('Schedule', 'r')
    lines = f.readlines()
    i = 1
    for line in lines:
        l = line.strip("\t")
        cpu = l[0]
        if cpu == i:
            l = line.strip("\t")
            u = l[0]
            u = u/4
            time = 10*u
            loops = time * 100 
            l = line.strip("\t")
            call(""
            # Spawn measuring 
            # Run loop
    fs.close()
