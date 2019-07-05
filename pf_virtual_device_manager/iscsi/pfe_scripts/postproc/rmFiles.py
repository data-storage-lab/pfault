#!/usr/bin/env python

#rm output-* files not in  a io file
#cd $LOG_DIR
#ls output-* > file_list.txt
#/PATH/THISFILE io_need_to_preserve.txt file_list.txt 

import os
import sys
import re
#from format_strace import lines2lists

def lines2lists(f):
    """input a file,
       convert each line to a list,
       output a list of lists"""

    ret_lines = [] 
    seperator = re.compile(r',| +|\n|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\"')
    lines = f.readlines()

    for line in lines:
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines




if __name__ == "__main__":
    #for fn in sys.argv[1]:

    io_list = [] 
    filename = sys.argv[1]
    for line in open(filename):#each line is an io#
        io_num = line.strip()
        io_list.append(io_num) #int for sorting later
     
    newck_file = sys.argv[2]
    for line in open(newck_file):#each line is "output.cut-19162" 
        filename = line.strip()
        line_list = filename.split('-')
        io_num = line_list[-1]
        if io_num not in io_list:
            print "remove "+ line
            os.remove(filename) 


        
