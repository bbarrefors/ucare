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

################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################

def main():
    """
    __main__


    """
    files = ['theoreticalPowerG', 'theoreticalPowerMW', 'theoreticalPowerHMWG']

    for filen in files:
        fd = open(filen, 'r')
        lines = fd.readlines()
        totPower = 0
        for line in lines:
            totPower += float(line.strip())
            totPower
        fd.close()
        fd = open(filen, 'a+')
        fd.write("%s\n" % (str(totPower),))
        fd.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
