#!/usr/bin/env python

#get unexpected IO:
#offset is in msync IO (imply mmapp region)
#offset is in fsync IO(, but fsync to a diff file from msync file
#/PATH/THISFILE io2file.dynamic.sim > result.txt 

import sys
import re
import tempfile
from operator import itemgetter
from format_strace import lines2lists
from subprocess import call, STDOUT
from collections import defaultdict
import random


def mark_suspicious_io(io_list):
    """
    mark suspicious io
    pattern: mmap region write to wrong fd
    offset is in msync IO (imply mmapp region)
    offset is in fsync IO(, but fsync to a diff file from msync file

    #file format:
    #IO# offset syscall filename
    #277 68682752 msync casket.tcb
    #278 68786176 msync casket.tcb
    #279 68682752 fsync casket.tcb
    #280 50912256 fsync casket.tcb
    #281 50916352 fsync casket.tcb
    """
    #get mmap offset/file via msync:
    mmap_region = {}
    for line in io_list:
        if line[2] == "msync":
            offset = line[1]
            filename = line[3]
            mmap_region[offset] = filename

    mmap_offsets = mmap_region.keys() 

    for line in io_list:
        if line[2] != "msync":
            offset = line[1]
            if offset in mmap_offsets:
                this_filename = line[3]
                msync_filename = mmap_region[offset]
                if this_filename != msync_filename:
                    line.append("SUSPICIOUS")

def get_suspicious_region(io_list):
    """
    get ios between a suspicious io and the next msync w/ the same offset

    #file format:
    #IO# offset syscall filename
    222 68682752 fsync casket.tcb.wal SUSPICIOUS
    223 73401344 fsync casket.tcb.wal
    224 50851840 fsync casket.tcb.wal
    225 50855936 fsync casket.tcb.wal

    """
    ret_list = []
    suspicious_started = False
    suspicious_addr = ""
    for line in io_list:
        if suspicious_started == False and len(line) == 5 and line[-1] == "SUSPICIOUS":
            #could be serveral continous SUSPICIOUS lines, only the addr of the 1st line are recorded for later msync matching
            #ret_list.append(line[:-1]) #don't include "SUSPICIOUS"
            ret_list.append(line) #don't include "SUSPICIOUS"
            suspicious_started = True
            suspicious_addr = line[1]

        elif len(line) == 4 and line[2] == "msync" and line[1] == suspicious_addr:
            suspicious_started = False 

        elif suspicious_started and line[2] != "msync":
            ret_list.append(line)
            
    return ret_list

def sample_list(io_list, percentage):
    """
    sample suspicous region to further reduce overhead
    """
    sampled_io_cnt = len(io_list) * int(percentage)/100
    population = range(0, len(io_list))

    k_sample_idx = random.sample(population, sampled_io_cnt)
    k_sample_idx.sort()

    ret_list = []
    for i in k_sample_idx:
        line = io_list[i]
        ret_list.append(line)

    return ret_list


if __name__ == "__main__":
    mapping_file = open(sys.argv[1]) 
    io_list = lines2lists(mapping_file)
    mark_suspicious_io(io_list)
    ret_list = get_suspicious_region(io_list)

    percentage = 50 #sample 50% IOs in suspicious region by default; 100 = sample all, same as no sampling
    ret_list = sample_list(ret_list, percentage)

    for line in ret_list:
        #print ' '.join(line) #print whole line
        print line[0]  #print only io num


    


    


