#!/usr/bin/env python

#select IO based on pattern
#print selected IO# to stdout
#/PATH/THISFILE io2ReqAndFile.sim.sim > pattern_io.txt 

import sys
import re
import tempfile
from operator import itemgetter
from format_strace import lines2lists
from subprocess import call, STDOUT
from collections import defaultdict

 



def get_repetitive_io(io_list):
    """
    pattern: repetitive offset (within an app file)
    default repetitive counts: 2

    IO 2 68682752 4096 REQ 2 68682752 4096 FILE NA
    ...
    IO X 68682752 4096 REQ X X868275X 4096 FILE NA //68682752 repetitive
    """
    app_io_list = [] #io belong to app
    for io in io_list:
        filename = io[-1]
        if filename != "fs-journal":# not fs io
            app_io_list.append(io)

    #count how many times each offset appears
    offset_count = defaultdict(int)
    for io in app_io_list:
        offset = io[2]
        offset_count[offset] += 1

    #save io with offset appearing more than threshould 
    repeat_count = 2 #default repeat count
    ret_list = []
    for io in app_io_list:
        offset = io[2]
        if offset_count[offset] >= repeat_count:
            #ret_list.append(io[1])        
            io_str = ' '.join(io)
            ret_list.append(io_str)        

    return ret_list



if __name__ == "__main__":
    mapping_file = open(sys.argv[1]) #io2ReqAndFile mapping
    io_list = lines2lists(mapping_file)

    #file format:
    #IO 1 REQ 1 SIZE 1024 IOOFFSET1KB 1 FILE NA
    #IO 2 REQ 2 SIZE 4096 IOOFFSET1KB 72193 FILE NA
    #IO 3 REQ 3 SIZE 1024 IOOFFSET1KB 72322 FILE NA
    #IO 4 REQ 4 SIZE 1024 IOOFFSET1KB 49411 FILE journal
    #IO 5 REQ 5 SIZE 2048 IOOFFSET1KB 49412 FILE journal

    result_io = get_repetitive_io(io_list)

    io_list = []
    for io in result_io:
        line_list = io.split() 
        line_list[1] = int(line_list[1]) #change IO # to int for sorting later
        io_list.append(line_list)

    io_list.sort(key=lambda x: x[1])
    for io_line in io_list:
        io_line[1] = str(io_line[1]) #change IO# back to str for join and print)
        #print ' '.join(io_line) #print whole line 
        print io_line[1] #print only io#
    


    


