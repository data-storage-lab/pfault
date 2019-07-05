#!/usr/bin/env python
import sys
import re

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

    useful_syscalls = ("write", "pwrite", "fdatasync", "fsync", \
                       "mmap", "msync", "open", "close")
    seperator = re.compile(r',| +|\n|\t|=+|!|#|\[|\]|\(|\)')
    lines = f.readlines()
    useful_lines = [] 

    for line in linelists:
        if len(line) >= 2:
            #append useful syscall line
            if line[1] in useful_syscalls:
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



def count_cuts(linelists):
    min_cut = 100000000
    max_cut = 0
    for line in linelists:
        if len(line) == 4 and line[0] == "Cut":
            this_cut = int(line[-1])
            if this_cut < min_cut:
                min_cut = this_cut
            if this_cut > max_cut:
                max_cut = this_cut
    cut_count = max_cut - min_cut  
    print "-----------------"
    print "max cutted io: " + str(max_cut) 
    print "min cutted io: " + str(min_cut)
    print "# of cuts : " + str(cut_count)

def count_mounterr(linelists):
    cnt = 0
    for line in linelists:
        if len(line) == 10 and line[1] == "wrong" and line[2] == "fs":
           cnt += 1 
    print "-----------------"
    print "# of mount errors: " + str(cnt)

def count_BDB_err(linelists):
    cnt = 0
    within_check_result = 0
    found_BDB_err = 0
    for line in linelists:
        if len(line) == 2 and line[0] == "APP" and line[1] == "CHECK":
            #print line
            within_check_result = 1

        if len(line) == 3 and line[0] == "APP" and line[1] == "CHECK" and line[2] == "DONE":
            #print line
            within_check_result = 0
            found_BDB_err = 0

        if within_check_result == 1 and found_BDB_err == 0:
            if any("BDB" in s for s in line):
                found_BDB_err = 1
                cnt += found_BDB_err
    print "-----------------"
    print "# of cuts report BDB error(s): " + str(cnt)
           

def count_BDB_APP1_incompTrans(linelists):
    cnt = 0
    within_check_result = 0
    found_incomp_trans = 0
   
    for line in linelists:
        if len(line) == 2 and line[0] == "APP" and line[1] == "CHECK":
            within_check_result = 1

        if len(line) == 3 and line[0] == "APP" and line[1] == "CHECK" and line[2] == "DONE":
            within_check_result = 0
            found_incomp_trans = 0

        if within_check_result == 1 and found_incomp_trans == 0:
            if any("good" in s for s in line):
                #print line
                good_cnt = int(line[1])
                bad_cnt = int(line[3])
                if good_cnt != 0 and bad_cnt != 0:
                    found_incomp_trans = 1
                    cnt += found_incomp_trans
        
    print "-----------------"
    print "# of BDB APP 1 incomplete transactions: " + str(cnt)


def count_BDB_APP1_I_expect(linelists):
    cnt = 0
    within_check_result = 0
    found = 0
   
    for line in linelists:
        if len(line) == 2 and line[0] == "APP" and line[1] == "CHECK":
            within_check_result = 1

        if len(line) == 3 and line[0] == "APP" and line[1] == "CHECK" and line[2] == "DONE":
            within_check_result = 0
            found = 0

        if within_check_result == 1 and found == 0:
            if any("expect" in s for s in line):
                found = 1
                cnt += found
        
    print "-----------------"
    print "# of BDB APP 1 'I expect ...': " + str(cnt)


def count_BDB_APP2_mt_special_incompTrans(linelists):
    cnt = 0
    within_check_result = 0
    found = 0
   
    for line in linelists:
        if len(line) == 2 and line[0] == "APP" and line[1] == "CHECK":
            within_check_result = 1

        if len(line) == 3 and line[0] == "APP" and line[1] == "CHECK" and line[2] == "DONE":
            within_check_result = 0
            found = 0

        if within_check_result == 1 and found == 0:
            #if any("error" in s for s in line):
            if line[0] == "error" and line[1] == "in":
                found = 1
                cnt += found
        
    print "-----------------"
    print "# of BDB APP 2 incomplete trans 'error in c[][][]': " + str(cnt)

def count_TC_err(linelists):
    cnt = 0
    within_check_result = 0
    found = 0
    for line in linelists:
        if len(line) == 2 and line[0] == "APP" and line[1] == "CHECK":
            within_check_result = 1

        if len(line) == 3 and line[0] == "APP" and line[1] == "CHECK" and line[2] == "DONE":
            within_check_result = 0
            found = 0

        if within_check_result == 1 and found == 0:
            if any("error" in s for s in line):
                found = 1
                cnt += found
    print "-----------------"
    print "# of cuts report TC error(s): " + str(cnt)
           
def count_TC_APP1_incompTrans(linelists):
    cnt = 0
    within_check_result = 0
    found = 0
   
    for line in linelists:
        if len(line) == 2 and line[0] == "APP" and line[1] == "CHECK":
            within_check_result = 1

        if len(line) == 3 and line[0] == "APP" and line[1] == "CHECK" and line[2] == "DONE":
            within_check_result = 0
            found = 0

        if within_check_result == 1 and found == 0:
            if line[0] == "loop_size" and line[2] == "good" and line[4] == "bad":
                good_cnt = int(line[3])
                bad_cnt = int(line[5])
                if good_cnt != 0 and bad_cnt != 0:
                    found = 1
                    cnt += found
        
    print "-----------------"
    print "# of TC incomplete transactions: " + str(cnt)


if __name__ == "__main__":
    for fn in sys.argv[1:]:
        f = open(fn)
        usefullines = lines2lists(f)
        count_cuts(usefullines)
        count_mounterr(usefullines)

        #BDB all APPs
        #count_BDB_err(usefullines)

        #BDB APP 1 single thread
        #count_BDB_APP1_incompTrans(usefullines)
        #count_BDB_APP1_I_expect(usefullines)

        #BDB APP 2 mt, dup special
        #count_BDB_APP2_mt_special_incompTrans(usefullines)

        #TC all APPs
        count_TC_err(usefullines)

        #TC APP 1 single thread
        count_TC_APP1_incompTrans(usefullines)
