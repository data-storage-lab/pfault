#!/usr/bin/env python

#rm the first two fields(i.e., abs TS, relative TS) of each line of syscall-io map.
#usage:
#./thisfile formatted.map.txt
import sys
import re
import operator

def lines2lists(f):
    """input a file,
       convert each line to a list,
       output a list of lists"""

    ret_lines = [] 
#    seperator = re.compile(r',| +|\n|:|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\"')
    seperator = re.compile(r',| +|\n|:|\t|#|\[|\]|\<|\>|\"')
    lines = f.readlines()

    for line in lines:
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines


def format_check_result(linelists):
    """ rm newck.output.* from the check result output """

    seperator = re.compile(r',|\.|-')
    lines = f.readlines()
    useful_lines = [] 

    for line in linelists:
        if len(line) >= 2:
            #append useful syscall line
            #if line[1] in useful_syscalls:
            newline = line[3:]
            head = line[0]
            #print head
            head_splitted = seperator.split(head)
            #head_filtered = filter(None, head_splitted)
            #print head_splitted
            cutio = int(head_splitted[-1])
            newline.insert(0, ':')
            newline.insert(0, cutio)
            useful_lines.append(newline)

#    sorted(useful_lines,key=lambda line: line[0])
#    sorted(useful_lines,key=operator.itemgetter(0), reverse=True)
    useful_lines.sort(key=operator.itemgetter(0))

    return useful_lines

def format_map_result(linelists):
    useful_lines = [] 
    for line in linelists:
        newline = line[2:]
        useful_lines.append(newline)

    return useful_lines


if __name__ == "__main__":
    for fn in sys.argv[1:]:
        f = open(fn)
        usefullines = lines2lists(f)

        #usefullines = format_check_result(usefullines)
        #for line in usefullines:
        #    head = 'cut@'+str(line[0])
        #    newline = [head] + line[1:]
        #    line_str = ' '.join(newline)
        #    print line_str
        
        usefullines = format_map_result(usefullines)
        for line in usefullines:
            line_str = ' '.join(line)
            print line_str
