#!/usr/bin/env python
import sys
import re
from format_strace import lines2lists


def insert_io2syscall(syscall_lists, io_lists):
    ret_lines = [] 
    io_idx = 0
    for syscall_line in syscall_lists:
        if len(syscall_line) > 1 and syscall_line[0].isdigit(): #not an empty line or x000
            #print syscall_line[0]
            ts_syscall = int(syscall_line[0])

            for io_line in io_lists[io_idx:]:
                if len(io_line) > 1: #not an empty line
                    #ts_io = int(io_line[1]) #[io_id, ts, ...]
                    ts_io = int(io_line[0]) #[ts, IO# ...]
                    if ts_io < ts_syscall:
                        #io_line.insert(0, 'IO#')
                        ret_lines.append(io_line)
                        io_idx += 1
                    else:
                        break

            ret_lines.append(syscall_line)

    #remaining io later than all syscall
    for io_line in io_lists[io_idx:]:
        ret_lines.append(io_line)

    return ret_lines


def reformat_list(linelists):
    ret_lines = []
    title_line = ['| absTS | ', 'relativeTS | ', 'IO   #  | ', 'Offset | ', 'Length | ', 'Data |']
    ret_lines.append(title_line)
    title_line = ['| absTS | ', 'relativeTS | ', 'Syscall | ', '...']
    ret_lines.append(title_line)
    first_line = linelists[0]
    first_ts = int(first_line[0])
    for line in linelists:
        new_line = line
        abs_ts = int(new_line[0])
        relative_ts = str(abs_ts - first_ts)
        new_line.insert(1, relative_ts)
        ret_lines.append(new_line)
        
    return ret_lines


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "No enough arguments! Usage: ./THISSCRIPT formatted_io_log formatted_strace_log"
        exit(0)
    f_io = open(sys.argv[1])
    f_syscall = open(sys.argv[2])
    syscall_lists = lines2lists(f_syscall)
    io_lists = lines2lists(f_io) 

    usefullines = insert_io2syscall(syscall_lists, io_lists) 
    usefullines = reformat_list(usefullines)

    for line in usefullines:
        line_str = ' '.join(line)
        print line_str
