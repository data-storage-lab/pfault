#!/usr/bin/env python

#rm call info from full io2ReqFileCall mapping
#/PATH/THISFILE io2ReqFilCall.sim > output.txt 

import sys
import re
import tempfile
from format_strace import lines2lists
from subprocess import call, STDOUT




def rm_call_info(trace_list): 
    """
    rm  call info from:
    1391577375342982 IO 3 68814848 1024 0000000000000000000000000000000000000000000000000000000000000000 REQ 3 OFFSET 68814848 SIZE 1024 FILE casket.tcb CALL fsync casket.tcb
    to:
    1391577375342982 IO 3 68814848 1024 0000000000000000000000000000000000000000000000000000000000000000 REQ 3 OFFSET 68814848 SIZE 1024 FILE casket.tcb 
    """
    ret_list = []
    for line in trace_list:
        new_line = line[:14]
        ret_list.append(new_line)

    return ret_list


if __name__ == "__main__":
    trace_file = open(sys.argv[1]) 
    trace_list = lines2lists(trace_file)

    trace_list = rm_call_info(trace_list)

    for line in trace_list:
        print ' '.join(line)


    


