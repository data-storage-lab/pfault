#!/usr/bin/env python

#simplify io2ReqAndFile map
#only keep REQ #, OFFSET1KB #, FILE name


import sys
import re
from format_strace import lines2lists



if __name__ == "__main__":

    fn = sys.argv[1]
    f = open(fn)
    flines = lines2lists(f)

    ret_lines = []
    for line in flines:
    #1391577375582680 IO 4 50596864 1024 98393bc004000000000000000004000000100000010000000500000001000000 REQ 4 OFFSET 50596864 SIZE 1024  FILE journal

        io_info = line[1:5] #"IO  4 50596864 1024"

        req_info = line[6:8] #"REQ 4 "
        req_offset = line[9] 
        remain = line[11:] #"1024  FILE journal"
        new_list = io_info + req_info + [req_offset] + remain 
        ret_lines.append(new_list)



    for line in ret_lines:
        line_str = ' '.join(line)
        print line_str
