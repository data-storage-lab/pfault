#!/usr/bin/env python

#simplify the output of map_io2file_dynamic.py
#/PATH/THISFILE io2file.dynamic-full.sim > output.txt 

import sys
import re
import tempfile
from format_strace import lines2lists
from subprocess import call, STDOUT




if __name__ == "__main__":
    trace_file = open(sys.argv[1]) 
    trace_list = lines2lists(trace_file)

    for line in trace_list:

        #only output some fields in IO lines
        #IO 1 1024 1024 0000800000020000000019990001d91c00007ff2000000010000000000000000 #1st IO no file mapping
        #IO 3 68814848 1024 0000000000000000000000000000000000000000000000000000000000000000 fsync casket.tcb
        if line[0] == "IO": 
            io_num = line[1]
            offset = line[2]
            syscall = line[-2]
            filename = line[-1]

            if len(line) == 5: #no  syscall and filename
                syscall = "NA"
                filename = "NA"
            print io_num + " " + offset + " " + syscall + " " + filename 



    


