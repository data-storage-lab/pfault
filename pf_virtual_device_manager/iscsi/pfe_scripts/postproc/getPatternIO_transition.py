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

 


def get_transition_io(io_list):
    """
    pattern: transition between files

    IO 2 68682752 4096 REQ 2 68682752 4096 FILE NA
    IO 3 68814848 1024 REQ 3 68814848 1024 FILE NA <----------
    IO 4 50596864 1024 REQ 4 50596864 1024 FILE fs-journal 
    IO 5 50597888 2048 REQ 5 50597888 2048 FILE fs-journal
    """
    tmp_list = []
    for this_io, next_io in zip(io_list, io_list[1::]):
        this_file = this_io[-1]
        next_file = next_io[-1]
        #if  this_file != "journal" and next_file == "journal":
        if  this_file != next_file and this_file != "fs-journal":#diff files, and not jumping from fs-journal to other files
            this_io_str = ' '.join(this_io)
            #next_io_str = ' '.join(next_io)
            tmp_list.append(this_io_str)
            #tmp_list.append(next_io_str) #some io may be added twice; rm dup later

    ret_list = list(set(tmp_list)) #rm duplicates
    #ret_list = sorted(ret_list)
    
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

    result_io = get_transition_io(io_list)

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
