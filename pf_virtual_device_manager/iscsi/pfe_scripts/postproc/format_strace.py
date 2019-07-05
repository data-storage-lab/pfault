#!/usr/bin/env python
import sys
import re
import operator

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


def get_usefullines(linelists):
    """input a list of lines (lists),
       keep useful syscall lines and data lines , 
       output a list of lines (lists)"""

    #useful_syscalls = ("write", "pwrite", "fdatasync", "fsync", \
    #                   "mmap","mmap2", "munmap", "unlink","msync", "open", "close")
    seperator = re.compile(r',| +|\n|\t|=+|!|#|\[|\]|\(|\)')
    lines = f.readlines()
    useful_lines = [] 

    for line in linelists:
        if len(line) >= 2:
            #append useful syscall line
            #if line[1] in useful_syscalls:

            #append all syscalls
            if line[0] != '|': # not data region

                #further simplify write/pwrite argument format
                if line[1] == "write" or line[1] == "pwrite":
                    #rm \x in data string argument
                    sep = re.compile(r'x|\\')
                    elem_list = sep.split(line[3])
                    elem_str = ''.join(elem_list)
                    line[3] = elem_str
                useful_lines.append(line)

            #append data region
            elif line[0] == '|':
                if len(line) > 16: # a full data line
                    data_line = line[2:18]
                else: # an incomplete data line
                    data_line = line[2:-2]
                #each data line becomes ['|', 'datastring']
                line_str = ''.join(data_line)
                line_str = '| ' + line_str
                data_line = line_str.split()
                useful_lines.append(data_line)

    return useful_lines


def rm_datalines(linelists):
    """input a list of lines (lists),
       rm data line beginning w/ '|', 
       output a list of lines (lists)"""

    ret_lines = [] 
    for line in linelists:
        if len(line) > 1:
            if line[0] == '|': # a data line
                pass
            else:
                ret_lines.append(line)

    return ret_lines 


def combine_datalines(linelists):
    """input a list of lines (lists),
       combine multiple data lines into one line, 
       output a list of lines (lists)"""
    ret_lines = [] 
    write_data = []
    write_data_str = ''
    write_data_line = []
    for line in linelists:
        if line[0] == '|': # a data line
            write_data.append(line[1])
        else:
            if len(write_data) > 0: #all data lines for this write has been collected
                write_data_str = ''.join(write_data)
                write_data_line.append('|')
                write_data_line.append(write_data_str)

                ret_lines.append(write_data_line)

                #write_data[:] = []
                #write_data_line[:] = []
                write_data = []
                write_data_line = []
                write_data_str = ''
            
            ret_lines.append(line)

    return ret_lines 


def convert_ts(linelists):
    """input a list of lines (lists),
       convert 1st elem of each line to ts in microsecons, 
       output a list of lines (lists)"""
    ret_lines = [] 
    seperator = re.compile(r'\.|\:')

    for line in linelists:
        if line[0] != '|': #a syscall line begin  w/ time
            splitted_time = seperator.split(line[0])
            if len(splitted_time) == 2: #a valid ts must be able to be splitted to two parts: "1392322823.218197"
                seconds=int(splitted_time[0])
                microseconds=int(splitted_time[1])
                ts = seconds*1000000 + microseconds
                #line[0] = str(ts)
                line[0] = ts #for sorting
                ret_lines.append(line)
        else:
            ret_lines.append(line)

    ret_lines.sort(key=operator.itemgetter(0))

    #change int ts back to str
    for line in ret_lines:
        line[0] = str(line[0])

    return ret_lines


def sort_syscalls(linelists):
    """
    sort syscal lines based on ts
    """
    ret_lines = []




#deprecated
def mv_pid(linelists):
    """mv pid from the beginning to the end of a line"""
    ret_lines = []

    for line in linelists:
        if len(line) > 1:
            if line[0] != '|':
                pid = line[0]
                new_line = line[1:]
                new_line.append(pid)
                ret_lines.append(new_line)

    return ret_lines



if __name__ == "__main__":
    for fn in sys.argv[1:]:
        f = open(fn)
        usefullines = lines2lists(f)
        usefullines = get_usefullines(usefullines)
        #usefullines = mv_pid(usefullines)
        usefullines = combine_datalines(usefullines)
        usefullines = convert_ts(usefullines)
        usefullines = rm_datalines(usefullines)
        for line in usefullines:
            line_str = ' '.join(line)
            print line_str
        
