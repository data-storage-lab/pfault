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



def rmNonASCII(f):
    lines = f.readlines()
    non_ascii_pattern = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\\]+|[^\s]+)")

    seperator = re.compile(r',| +|\n|\t|!|#|\[|\]|\(|\)|\<|\>|\"|\|')

    ret_lines = []  
    for line in lines:
        ascii_line = non_ascii_pattern.sub('', line)
        newline = ascii_line.rstrip()
        line_splitted = seperator.split(newline)
        line_filtered = filter(None, line_splitted)
        #print line_filtered 
        ret_lines.append(line_filtered)

    return ret_lines

def rmUselessLines(lines):
    """further rm useless lines for SQLServer output"""

    ret_lines = []
    for line in lines:
        if len(line) == 0:#empty line
            pass
        elif len(line) == 3 and line[1] == "rows": #"1 rows affected"
            pass
        elif len(line) >= 1 and "--------" in line[0]: #"----- ------"
            pass
        elif len(line) >= 3 and line[0] == "Changed": #"Changed database context to 'hdcdb'."
            pass
        else:
            ret_lines.append(line)

    return ret_lines


if __name__ == "__main__":

    fn = sys.argv[1]
    f = open(fn)
    lines = rmNonASCII(f)
    lines = rmUselessLines(lines)
    for line in lines:
        line_str = ' '.join(line)
        print line_str


