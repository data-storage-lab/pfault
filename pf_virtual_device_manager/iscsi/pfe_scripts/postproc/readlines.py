#!/usr/bin/env python
#read and print each line of a file
#./THISFILE file_to_print

import sys
import re
import fileinput
import os
import time
import datetime
import calendar
import unicodedata

def lines2lists(f):
    """input a file,
       convert each line to a list,
       output a list of lists
    """

    ret_lines = []  
    seperator = re.compile(r',| +|\n|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\"|\|')
    lines = f.readlines()

    for line in lines:
        print line
        line = line.rstrip() #rm carriage return from windows file
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines

def rmNonASCII(f):
    lines = f.readlines()
    non_ascii_pattern = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\\]+|[^\s]+)")

    seperator = re.compile(r',| +|\n|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\"|\|')

    ret_lines = []  
    for line in lines:
        ascii_line = non_ascii_pattern.sub('', line)
        newline = ascii_line.rstrip()
        line_splitted = seperator.split(newline)
        line_filtered = filter(None, line_splitted)
        #print newline
        print line_filtered 



if __name__ == "__main__":

    fn = sys.argv[1]
    f = open(fn)
    rmNonASCII(f)
    #lines = lines2lists(f)
    #for line in lines:
    #    print line


