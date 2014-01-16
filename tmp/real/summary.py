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
    tasks = [100]
    util = [20, 35]
    alg = ['G', 'MW', 'HWF']

    files = []

    for t in tasks:
        for u in util:
            for a in alg:
                files.append('t%du%da%s' % (t, u, a))
    
    for filen in files:
        fd = open(filen, 'a+')
        lines = fd.readlines()
        totPower = 0
        for line in lines:
            totPower += float(line.strip())
        fd.write("%s\n" % (str(totPower),))
        fd.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())

