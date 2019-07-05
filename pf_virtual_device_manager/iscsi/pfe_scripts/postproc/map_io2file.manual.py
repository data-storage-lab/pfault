#!/usr/bin/env python
#map io to db files based on io offset and file blocks
#usage:
#./thisfile io_offsets

import sys
import re
from format_strace import lines2lists


#generate block# in range [low_bound, up_bound]
def gen_block_range(low_bound, up_bound):
    ret_list=[]
    for blk in range(low_bound, up_bound+1):
        ret_list.append(str(blk))
    return ret_list

if __name__ == "__main__":
    #if len(sys.argv) < 3:
    #    print "No enough arguments! Usage: ./THISSCRIPT io_offsets"
    #    exit(0)
    f_io = open(sys.argv[1])
    #lines = f_io.readlines()
    #io_list = []
    #for line in lines:
    #    io_list.append(str(line))

    #read one io each line (without reading the newline)
    io_list = f_io.read().splitlines()
    #for elem in io_list:
    #    print elem

    #io_list = lines2lists(f_io) 

    #=====================TC
    #TC: casket.tcb
    name1 = "casket.tcb"
    first1 = int(39937)
    last1 = int(40097)
    block_range_1 = gen_block_range(first1, last1)


    #TC: casket.tcb.wal
    name2 = "casket.tcb.wal"
    first2 = int(35841)
    last2 = int(35852)
    block_range_2 = gen_block_range(first2, last2)

    #TC: directory myEnvironment
    name3 = "myEnvironment"
    first3 = int(39425)
    last3 = int(39425)
    block_range_3 = gen_block_range(first3, last3)

#    #====================SQLite
#    name1 = "abc.db"
#    first1 = int(1545)
#    last1 = int(1585)
#    block_range_1 = gen_block_range(first1, last1)
#
#    name2 = "abc.db-journal"
#    first2 = int(4097)
#    last2 = int(4114)
#    block_range_2 = gen_block_range(first2, last2)
#
#    #none
#    name3 = " "
#    first3 = int(0)
#    last3 = int(0)
#    block_range_3 = gen_block_range(first3, last3)


    #==================== filesystem's
    #fs journal
    name_j = "fs journal"
    first_j = int(49411)
    last_j = int(53523)
    block_range_j = gen_block_range(first_j, last_j)

    #default: fs  
    name_default = "fs"

    new_io_list = []
    for io in io_list:
        io_str = str(io)
        if io_str in block_range_1:
            tmp = str(io) + ' ' + name1
        elif io in block_range_2:
            tmp = str(io) + ' ' + name2
        elif io in block_range_3:
            tmp = str(io) + ' ' +  name3
        elif io in block_range_j:
            tmp = str(io) + ' ' +  name_j
        else:
            tmp = str(io) + ' ' + name_default

        new_io_list.append(tmp)

            
    for elem in new_io_list:
       print elem
            





