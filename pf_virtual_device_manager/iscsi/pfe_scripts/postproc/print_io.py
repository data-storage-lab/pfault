#!/usr/bin/env python

#print the content of an IO
#usage:
#./THISFILE pfe_io_head_split_log.od  pfe_io_data_log.work.od IO#_to_print 

import sys
import re
from format_strace import lines2lists
import format_iolog 


def get_io_content(head_linelists, data_linelists, io_num):
    ret_lines = []
    this_head_line = head_linelists[io_num-1]
    ret_lines.append(this_head_line)

    #head line format: "ts 'IO#' io#  disk_offset length datalog_offset"
    datalog_offset = int(this_head_line[-1]) #get datalog_offset of this IO
    first_dataline_num = datalog_offset/32 #each data_line is 32 bytes

    data_length = int(this_head_line[-2])
    data_line_cnt = data_length/32
    last_dataline_num = first_dataline_num + data_line_cnt - 1

    useful_datalines = data_linelists[first_dataline_num: last_dataline_num + 1] 

    for line in useful_datalines:
        line = line[1:] #line[0] is address, line[1] is content
        ret_lines.append(line)
        
    return ret_lines

if __name__ == "__main__":
    io_head_fn = sys.argv[1]
    io_data_fn = sys.argv[2]
    io_num = int(sys.argv[3])

    head_f = open(io_head_fn)
    head_lines = lines2lists(head_f)
    head_lines = format_iolog.formatline(head_lines)
    head_lines = format_iolog.reformatline(head_lines)
    #for line in head_lines:
    #    line_str = ' '.join(line)
    #    print line_str


    data_f = open(io_data_fn)
    data_lines = lines2lists(data_f)
    #data_lines = format_iolog.format_dataline(data_lines)
    #for line in data_lines:
        #line_str = ' '.join(line)
        #print line_str


    lines = get_io_content(head_lines, data_lines, io_num)
    for line in lines:
        #line_str = ' '.join(line)
        #print line_str
        print line
