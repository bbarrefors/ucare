#!/usr/bin/python26 -B
"""
_summary_

Created by Bjorn Barrefors on 31/10/2013

University of Nebraska-Lincoln
"""
###############################################################################
#                                                                             #
#                             S I M U L A T O R                               #
#                                                                             #
###############################################################################

import sys
import csv

################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################

def main():
    """
    __main__


    """
    numTasks = [250, 350]
    totUtils = [25]
    algs = ['HyMWGA', 'BaB']

    files = []

    for u in totUtils:
        for t in numTasks:
            for a in algs:
                files.append('u%dt%da%s' % (u, t, a))
    power = []
    for filen in files:
        fd = open(filen, 'r')
        lines = fd.readlines()
        totPower = 0
        for line in lines:
            totPower += float(line.strip())
            totPower
        fd.close()
        power.append(totPower)
    with open('power.csv', 'ab') as csvfile:
        wrt = csv.writer(csvfile)
        wrt.writerow(power)
    return 0

if __name__ == '__main__':
    sys.exit(main())
