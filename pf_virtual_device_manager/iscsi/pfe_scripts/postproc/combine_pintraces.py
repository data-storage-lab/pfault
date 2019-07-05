#!/usr/bin/env python
import sys
import re
import operator
import glob
import os

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



if __name__ == "__main__":
    log_dir_name = sys.argv[1]

    output_linelist = []

    os.chdir(log_dir_name)
    #for filename in glob.glob("strace-worklog.txt.*"):
    for filename in glob.glob("pintool.log.wk*"):

        seperator = re.compile(r',|\.')
        filename_splitted = seperator.split(filename)
        pid = filename_splitted[2:]
        #print pid[0]
        
        full_filename = log_dir_name+'/'+filename
        #print full_filename 
        file = open(full_filename) 

        seperator = re.compile(r',| +|\n|:|\t|#|\[|\]|\<|\>|\"')
        lines = file.readlines()

        for line in lines:
            line_splitted = seperator.split(line)
            line_filtered = filter(None, line_splitted)
            #if line_filtered[0] != '|':
            if line_filtered[0] != 'Pin':
                new_line = line_filtered + pid
            else:
                new_line = line_filtered
            output_linelist.append(new_line)


    for line in output_linelist:
        line_str = ' '.join(line)
        print line_str


