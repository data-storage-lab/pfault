#!/usr/bin/env python

#intersect pattern io files
#/PATH/THISFILE pattern_io_1.txt pattern_io_2.txt ...

import sys
import re
from format_strace import lines2lists

def intersect(a, b):
    return list(set(a) & set(b))


if __name__ == "__main__":
    #for fn in sys.argv[1]:

    list1 = [] 
    filename = sys.argv[1]
    for line in open(filename):#each line is an io#
        io_num = line.strip()
        list1.append(int(io_num)) #int for sorting later
     
    combined_list=list1
    io_seq_files = sys.argv[2:]
    for filename in io_seq_files:
        listN = []
        for line in open(filename):#each line is an io#
            io_num = line.strip()
            listN.append(int(io_num)) #int for sorting later
        combined_list = intersect(combined_list, listN) 


    #sort
    combined_list.sort()

        
    for line in combined_list:
        print line
