#!/usr/bin/env python

#separate each rank to different files
#/PATH/THISFILE patternIO.rank.txt 

import sys
import re
from format_strace import lines2lists
from collections import Counter

def separate_ranks(io_list):
    """
    IO# rank# PATTERNNAME1 PATTERNNAME2 ...:
    7 3 patternIO_transition.txt patternIO_repetitive.txt patternIO_head.txt
    11 3 patternIO_transition.txt patternIO_repetitive.txt patternIO_head.txt
    """

    ranks_map = {} #rank#, "io1 io2 io3 ..."    
    for line in io_list:
        io_num = line[0]
        rank = line[1]
        if rank in ranks_map:
            ranks_map[rank] = ranks_map[rank] + " " + io_num
        else:
            ranks_map[rank] = io_num

    for rank,io_seq in ranks_map.items():
        filename = "patternIO.rank-" + rank
        io_list = io_seq.split()
        with open(filename, 'w+') as f:
            for io in io_list:
                f.write(io+'\n')
            



if __name__ == "__main__":

    io_rank_file = open(sys.argv[1])
    io_list = lines2lists(io_rank_file)
    separate_ranks(io_list)



