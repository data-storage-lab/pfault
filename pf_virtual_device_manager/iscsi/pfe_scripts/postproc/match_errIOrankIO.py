#!/usr/bin/env python

#compare rank IO seq to err IO seq, see if rank IO can detect err
#grep Err newck* > err_file
#/PATH/THISFILE err_file patternIO.rank-3

import sys
import re
#from format_strace import lines2lists
#from collections import Counter

def lines2lists(f):
    """input a file,
       convert each line to a list,
       output a list of lists"""

    ret_lines = [] 
    seperator = re.compile(r',| +|\n|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\\|\:|-|\"')
    lines = f.readlines()

    for line in lines:
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines



if __name__ == "__main__":

    err_file = open(sys.argv[1])
    err_linelists = lines2lists(err_file)
   
    io_seq_file = open(sys.argv[2])
    io_linelists = lines2lists(io_seq_file)
   
    
    result_list = [] 
    errIO_map = {} #IO#, ErrType

    for line in err_linelists:
    #['newck.output.cut', '641', 'PFEErrCode', '0.1', 'DDD', 'ERR', 'ReadByKey', '0', 'or', 'ReadByCursor', '0', 'Expected', '1020']
        if len(line) >= 6 and "newck" in line[0]:
            io_num = line[1]
            err_type = line[4]

            if io_num in errIO_map:
                val_str = errIO_map[io_num] + " " + err_type #add this type to the io
                errIO_map[io_num] = val_str 
            else:
                errIO_map[io_num] = err_type

    for line in io_linelists:
        io_num = line[0]
        if io_num in errIO_map:
            print io_num + " " + errIO_map[io_num]



