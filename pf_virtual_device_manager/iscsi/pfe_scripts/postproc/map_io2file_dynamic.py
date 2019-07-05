#!/usr/bin/env python

#map each io to a fd based on strace
#NOTE: sys call trace is based on strace. pintool trace has a different format, and is not supported yet
#/PATH/THISFILE formatted.map.sim > output.txt 

import sys
import re
import tempfile
from format_strace import lines2lists
from subprocess import call, STDOUT




def prune_calls(trace_list): 
    """
    prune unnecessary calls
    """
    ret_list = []
    usefull_calls = ['fsync', 'fdatasync', 'open', 'close', 'msync', 'mmap', 'mmap2', 'munmap', 'link', 'unlink', 'unlinkat']
    for line in trace_list:
        if len(line) > 1:
            if line[0] == "IO": #IO line
                ret_list.append(line)
            elif line[0] in usefull_calls:
                ret_list.append(line)
            else:
                pass

    return ret_list

def map_msync2fd(trace_list):
    """
    map msync to fd in mmap based on address
    """

    for i, i_line in enumerate(trace_list):
        #['msync', '0x7fa40cc6c000', '131252', 'MS_SYNC', '0', '0.151759', '20475']
        if i_line[0] == "msync":
            i_addr = i_line[1]
            i_fd = ""

            #traverse reversely to find the closest matching mmap (return same addr)
            #only consider lines before this line
            for j_line in reversed(trace_list[:i]): 
                if j_line[0] == "mmap" or j_line[0] == "mmap2":  
                    #['mmap', 'NULL', '131252', 'PROT_READ|PROT_WRITE', 'MAP_SHARED', '3', '0', '0x7fa40cc6c000', '0.000015', '20474']
                    if j_line[7] == i_addr: #addr match
                        i_fd = j_line[5]
                        break
 
            i_line.append(i_fd)



def map_sync2file(trace_list):
    """
    map fd number in fsync/fdatasync and msync(added w/ fd) to filename in open()
    """

    for i, i_line in enumerate(trace_list):
        i_name = i_line[0]

        #['fsync', '3', '0', '0.664654', '20475']
        if i_name == "fsync" or i_name == "fdatasync":
            i_fd = i_line[1]
            i_filename = "" 

            #traverse reversely to find the closest matching open (return same fd)
            #only consider lines before this line
            for j_line in reversed(trace_list[:i]): 
                if j_line[0] == "open":  
                    #['open', '/mnt/iscsi-fs/myEnvironment/casket.tcb', 'O_RDWR|O_CREAT', '0644', '3', '0.000016', '20474'] #has mode, so fd is at [4]
                    #['open', '/sys/devices/system/cpu/online', 'O_RDONLY|O_CLOEXEC', '6', '0.000027', '20475'] #no mode, so fd is at [3]
                    if j_line[3] == i_fd or j_line[4] == i_fd: #fd match; fd could be either at [3] or [4]
                        i_filename = j_line[1]
                        break
                        
            fullname_list = i_filename.split('/') #fullname: "/mnt/iscsi-fs/myEnvironment/casket.tcb"
            basename = fullname_list[-1] #basename:"casket.tcb"
            #i_line.append("FILE")
            i_line.append(basename)


        #['msync', '0x7fa40cc6c000', '131252', 'MS_SYNC', '0', '0.151759', '20475', '3'] #fd is added at the end by map_msync2fd()
        elif i_name == "msync":
            i_fd = i_line[-1]
            i_filename = "" 

            #traverse reversely to find the closest matching open (return same fd)
            #only consider lines before this line
            for j_line in reversed(trace_list[:i]): 
                if j_line[0] == "open":  
                    #['open', '/mnt/iscsi-fs/myEnvironment/casket.tcb', 'O_RDWR|O_CREAT', '0644', '3', '0.000016', '20474'] #has mode, so fd is at [4]
                    #['open', '/sys/devices/system/cpu/online', 'O_RDONLY|O_CLOEXEC', '6', '0.000027', '20475'] #no mode, so fd is at [3]
                    if j_line[3] == i_fd or j_line[4] == i_fd: #fd match; fd could be either at [3] or [4]
                        i_filename = j_line[1]
                        break
                        
            fullname_list = i_filename.split('/') #fullname: "/mnt/iscsi-fs/myEnvironment/casket.tcb"
            basename = fullname_list[-1] #basename:"casket.tcb"
            #i_line.append("FILE")
            i_line.append(basename)

        else:
            pass

def map_io2file_dynamic(trace_list):

    for i, i_line in enumerate(trace_list):
        if i_line[0] == "IO": #an IO line
            i_syscall = ""
            i_filename = ""

            #travese previous lines reversely
            for j_line in reversed(trace_list[:i]): 
                if j_line[0] == "fsync" or j_line[0] == "fdatasync" or j_line[0] == "msync":  
                    i_syscall = j_line[0]
                    i_filename = j_line[-1]
                    break

            i_line.append(i_syscall)
            i_line.append(i_filename)



if __name__ == "__main__":
    trace_file = open(sys.argv[1]) 
    trace_list = lines2lists(trace_file)

    trace_list = prune_calls(trace_list)
    map_msync2fd(trace_list)
    map_sync2file(trace_list)
    map_io2file_dynamic(trace_list)

    for line in trace_list:

        #only output IO lines
        #if line[0] == "IO":
        #    io_num = line[1]
        #    offset = line[2]
        #    syscall = line[-2]
        #    filename = line[-1]
        #    print io_num + " " + offset + " " + syscall + " " + filename 

        #output all lines (easir for finding false msync io)
        print ' '.join(line)


    


