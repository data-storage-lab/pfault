#!/usr/bin/env python

#for drawing io err trend of an IO sequence: err ios "1",  other ios "0"
#usage:
#./THIS_PY ErrResultFile TotalIO

#e.g.:
#./print_err_trend.py /home/zhengm/logs-folder/logs-tc-wkld4_THR-2-TXN-10-KEY-10_fail-0-unseri-small-fs-xfs-cutopt-EXHAUSTIVE_CUT-100.131010112829/tmp 1573

import sys
import re

def lines2lists(f):
    """input a file,
       convert each line to a list,
       output a list of lists"""

    ret_lines = [] 
    seperator = re.compile(r',| +|-|:|\n|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\"')
    lines = f.readlines()

    for line in lines:
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines


def getErrIOs(lines):
    """ get err ios"""
    ret_lines = []
    for line in lines:
        ret_lines.append(int(line[1]))

    return ret_lines

if __name__ == "__main__":
    fn = sys.argv[1]
    f = open(fn)
    usefullines = lines2lists(f)
    usefullines = getErrIOs(usefullines)
   
    tot_ios = int(sys.argv[2])
    for i in range(1, tot_ios+1):
        if i in usefullines:
            print 1
        else:
            print 0
    
    #for line in usefullines:
        #line_str = ' '.join(line)
        #print line_str
        #print line
    
