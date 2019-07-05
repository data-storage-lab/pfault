#!/usr/bin/env python

#merge io2req map and io2file map
#./THISFILE io2req.sim io2file.sim

import sys
import re
from format_strace import lines2lists


if __name__ == "__main__":
    #for fn in sys.argv[1]:

    io2req_fn = sys.argv[1]
    io2req_f = open(io2req_fn)
    io2req_lines = lines2lists(io2req_f)

    io2file_fn = sys.argv[2]
    io2file_f = open(io2file_fn)
    io2file_lines = lines2lists(io2file_f)

    #for i in len(io2req_lines):
    #    io2file_line = io2file_lines[i]
    #    if len(io2file_line) == 2: #offset, filename
    #        filename = io2file_line[1]
    #        append_str = " FILE= " + filename
    #        io2req_line[i].append(append_str)
    io_num = 0
    for io2req, io2file in zip(io2req_lines, io2file_lines):
        #add IO # to the beginning
        #io_num += 1;
        #io_num_str = "IO " + str(io_num)
        #io2req = [io_num_str] + io2req

        #add file name to the end
        #filename = io2file[-1]
        #append_str = " FILE " + filename
        #io2req.append(append_str)

        #add file name and call info to the end
        # 8 50600960 fs-journal CALL fsync casket.tcb.wal

        file_and_call = io2file[2:]
        append_list = ["FILE"] + file_and_call
        append_str = ' '.join(append_list)
        io2req.append(append_str)

        
    for line in io2req_lines:
        line_str = ' '.join(line)
        print line_str

    


#    for line in head_lines:
#        line_str = ' '.join(line)
#        print line_str

#    for line in usefullines:
#        print line


