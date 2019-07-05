#!/usr/bin/env python

#./THISFILE IO_HEAD_LOG IO_DATA_LOG DATA_LINE_WIDTH
import sys
import re
from format_strace import lines2lists

def formatline(linelists):
    """input a list of lines (lists),
       rm useless elems in each line , 
       output a list of lines (lists)"""
    ret_lines = []
    for line in linelists:#skip 1st line (total io cnt line)
        if int(line[-1]) == 101010101010:
            #line format: "ADDR IO# id ts offset length datalog_offset cmd_type data_dir MARKER"
            line = line[1:-1] #rm ADDR and MARKER
            ret_lines.append(line)

    return ret_lines

def reformatline(linelists):
    ret_lines = []
    for line in linelists:
        io_num = line[0]
#        new_line = line[1:-3] #rm datalog_offset and cmd_type fields
        new_line = line[1:-2] #rm cmd_type field
        new_line.insert(1, io_num)
        new_line.insert(1, "IO#")
        ret_lines.append(new_line)

    return ret_lines

def format_dataline(linelists):
    ret_lines = []
    for line in linelists:
        #data_str = ''.join(line[1:-1]) #line[0] is od address
        data_str = ''.join(line[1:]) #line[0] is od address
        new_line = []
        new_line.insert(0, line[0])
        new_line.insert(1, data_str)
        ret_lines.append(new_line)

    return ret_lines


def append_io_data(head_linelists, data_linelists, dataline_width):
    ret_lines = []
    #append the first dataline to each IO 
    for line in head_linelists:
        offset = int(line[-1]) #get datalog_offset of this IO
        data_line_num = offset/dataline_width #each dataline is 32 bytes
#        new_line = line[:] 
        new_line = line[:-1] # rm datalog_offset

#        new_line.append(data_line_num) 
#        new_line.append(data_linelists[data_line_num]) #append both dataline addr and data
        new_line.append(data_linelists[data_line_num][1]) # append only dataline data)
        ret_lines.append(new_line)

    return ret_lines

if __name__ == "__main__":
    #for fn in sys.argv[1]:
    io_head_fn = sys.argv[1]
    head_f = open(io_head_fn)
    head_lines = lines2lists(head_f)
    head_lines = formatline(head_lines)
    head_lines = reformatline(head_lines)
#    for line in head_lines:
#        line_str = ' '.join(line)
#        print line_str

    io_data_fn = sys.argv[2]
    dataline_width = int(sys.argv[3])

    data_f = open(io_data_fn)
    data_lines = lines2lists(data_f)
    data_lines = format_dataline(data_lines)
#    for line in usefullines:
#        print line

    lines = append_io_data(head_lines, data_lines, dataline_width)
    for line in lines:
        line_str = ' '.join(line)
        print line_str

