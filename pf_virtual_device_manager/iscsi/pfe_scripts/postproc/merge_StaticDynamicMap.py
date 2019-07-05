#!/usr/bin/env python

#merge io2file.static.sim and io2file.dynamic.sim
#/PATH/THISFILE io2file.static.sim io2file.dynamic.sim

import sys
import re
from format_strace import lines2lists


if __name__ == "__main__":
    #for fn in sys.argv[1]:

    io2file_static_fn = sys.argv[1]
    static_f = open(io2file_static_fn)
    static_lines = lines2lists(static_f)

    io2file_dynamic_fn = sys.argv[2]
    dynamic_f = open(io2file_dynamic_fn)
    dynamic_lines = lines2lists(dynamic_f)

    combined_list = []
    for stat_l, dyna_l in zip(static_lines, dynamic_lines):
        #static line: 7 72877056 NA   
        #dynamic line: 7 72877056 fsync casket.tcb.wal

        #stat_l.insert(2, "  #STATIC_FILE: ")
        dynamic_info = [" CALL"] + dyna_l[2:] 
        #dynamic_info = dyna_l[2:] 
        new_line = stat_l + dynamic_info
        combined_list.append(new_line)
        
    for line in combined_list:
        line_str = ' '.join(line)
        print line_str
