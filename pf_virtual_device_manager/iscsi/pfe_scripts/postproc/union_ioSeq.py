#!/usr/bin/env python

#union pattern io files
#/PATH/THISFILE pattern_io_1.txt pattern_io_2.txt ...

import sys
import re
from format_strace import lines2lists


if __name__ == "__main__":
    #for fn in sys.argv[1]:

    combined_list = [] 
    io_seq_files = sys.argv[1:]
    for filename in io_seq_files:
        for line in open(filename):#each line is an io#
            io_num = line.strip()
            combined_list.append(int(io_num)) #int for sorting later
            #print combined_list

    #rm duplicates
    combined_list = list(set(combined_list))

    #sort
    combined_list.sort()

        
    for line in combined_list:
        print line
