#!/usr/bin/env python

#select IO based on pattern
#pattern: head of a request
#/PATH/THISFILE io2ReqAndFile.sim.sim > pattern_io.txt 

import sys
import re
import tempfile
from operator import itemgetter
from format_strace import lines2lists
from subprocess import call, STDOUT
from collections import defaultdict

 


def get_head_io(io_list):
    """
    pattern: head of a request; default head size = 4KB (1 IO) 

    IO 2 68682752 4096 REQ 2 68682752 4096 FILE NA
    IO 3 68814848 1024 REQ 3 68814848 1024 FILE NA <---------- head of req 3
    IO 4 50596864 1024 REQ 3 50596864 1024 FILE NA 
    IO 5 50597888 2048 REQ 4 50597888 2048 FILE fs-journal
    """
    large_req_io_cnt = 4 #only consider >=large_req_io_cnt IOs as large request
    head_length = 1 #only consider the first head_lenth IOs as head of a large request 
    isLarge = False
    head_cnt = 0 
    
    tmp_list = []
    for this_io, next_io in zip(io_list, io_list[1::]):
        this_req = this_io[5]
        next_req = next_io[5]
        if  this_req != next_req: #next line is a new req
            #add next line to result
            next_io_str = ' '.join(next_io)
            tmp_list.append(next_io_str) #some io may be added twice; rm dup later

            next_req_size = int(next_io[7])
            next_req_io_cnt = next_req_size/4096 #each IO is 4096 by default
            if next_req_io_cnt >= large_req_io_cnt: #large req
                isLarge = True 
                head_cnt = 0
                continue
            else:
                isLarge = False
        elif isLarge and head_cnt < head_length: #this and next are same req, but this is a large req; head = 0, 1, 2
            this_io_str = ' '.join(this_io)
            tmp_list.append(this_io_str) #some io may be added twice; rm dup later
            head_cnt += 1;

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

    result_io = get_head_io(io_list)

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
