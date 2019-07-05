#!/usr/bin/env python

#rm lib calls from pintrace
#./THISFILE PIN_TRACE_FILE
import sys
import re
import operator

def lines2lists(f):
    """input a file,
       convert each line to a list,
       output a list of lists"""

    ret_lines = [] 
    seperator = re.compile(r',| +|\n|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\|\:| ')
    lines = f.readlines()

    for line in lines:
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines


def get_usefullines(linelists):
    """input a list of lines (lists),
       keep useful syscall lines and data lines , 
       output a list of lines (lists)"""

    useful_lines = [] 

    for line in linelists:
        if len(line) >= 4:
            #if line[3] != 'libc.so.6' and line[3] != "libpthread.so.0" : 
            #for check log, no relatvieTS field, so rm [2]
            if line[2] != 'libc.so.6' and line[2] != "libpthread.so.0" : 
                useful_lines.append(line)

    return useful_lines


if __name__ == "__main__":
    for fn in sys.argv[1:]:
        f = open(fn)
        usefullines = lines2lists(f)
        usefullines = get_usefullines(usefullines)
        for line in usefullines:
            line_str = ' '.join(line)
            print line_str
        
