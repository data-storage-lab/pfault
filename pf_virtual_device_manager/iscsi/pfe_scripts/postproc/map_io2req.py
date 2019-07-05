#!/usr/bin/env python

#map each splitted IO (default 4KB) to the original request (maybe > 4KB)
#./THISFILE formatted_io IO_HEAD_LOG 
#./THISFILE formatted.io.txt pfe_io_header_log.work.od > io2req.txt 

import sys
import re
from format_strace import lines2lists



if __name__ == "__main__":
    #for fn in sys.argv[1]:
    formatted_io_fn = sys.argv[1]
    formatted_io_f = open(formatted_io_fn)
    formatted_io_lines = lines2lists(formatted_io_f)

    req_fn = sys.argv[2]
    req_f = open(req_fn)
    req_lines = lines2lists(req_f)

    for io_line in formatted_io_lines:
        #1392469377972388 IO# 2 2099200 1024 0000000000000000002000000000000020202020000000000000000000000000
        ts = io_line[0]
#        io_offset = io_line[3]

        for req_line in req_lines:
            if int(req_line[-1]) == 101010101010:
            #line format: "ADDR REQUEST# ts offset length datalog_offset cmd_type data_dir MARKER"
            #0000128                    2     1392469377972388              2099200                 1024                 1024                   42                    1         101010101010
                if ts == req_line[2]:
                    req_num = req_line[1]
                    req_offset = req_line[3]
                    req_length = req_line[4]
                    append_str = "REQ " + req_num + ", OFFSET " + req_offset + ", SIZE " + req_length;# + ", IOOFFSET1KB= " + str(int(req_offset)/1024);
                    io_line.append(append_str)
                    break

        
    for line in formatted_io_lines:
        line_str = ' '.join(line)
        print line_str


#    for line in head_lines:
#        line_str = ' '.join(line)
#        print line_str

#    for line in usefullines:
#        print line


