#!/usr/bin/env python

#union pattern io files
#/PATH/THISFILE pattern_io_1.txt pattern_io_2.txt ...

import sys
import re
from format_strace import lines2lists
from collections import Counter


if __name__ == "__main__":
    #for fn in sys.argv[1]:

    combined_list = [] 
    io2file_map = {}
    io_seq_files = sys.argv[1:]

    for filename in io_seq_files:
        for line in open(filename):#each line is an io#
            io_num = line.strip()
            combined_list.append(int(io_num)) #int for sorting later

            if io_num in io2file_map:
                val_str = io2file_map[io_num] + " " + str(filename) #add this filename to the io
                io2file_map[io_num] = val_str 
            else:
                io2file_map[io_num] = str(filename) 

    #sort
    #combined_list.sort()
    combined_list = Counter(combined_list).most_common()

    for line in combined_list:
        #(IO#, count):
        #(11, 3)
        #(15, 3)
        #print line
        io_num = str(line[0])
        io_cnt = str(line[1])
        files = io2file_map[str(io_num)]
        print io_num + " "  + io_cnt + " " + files


