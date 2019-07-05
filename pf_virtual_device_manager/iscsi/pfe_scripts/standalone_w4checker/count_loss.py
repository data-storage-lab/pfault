#!/usr/bin/env python

import sys
import re
import fileinput
import os
import time
import datetime
import calendar

def lines2lists(f):
    """input a file,
       convert each line to a list,
       output a list of lists
    """

    ret_lines = [] 
    seperator = re.compile(r',| +|\n|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\"|\|')
    lines = f.readlines()

    for line in lines:
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines


def get_DErr_lines(linelists):
    """
    get DDD-ERR lines from all Err
    """

    ret_lines = [] 
    for line in resultlines:
        #['./newck.output.cut-2826:', 'PFEErrCode', '12:', 'DDD-ERR', 'thr-10-txn-9', 'BEFORE', 'cut', 'not', 'committed']
        #./newck.output.cut-2742:#PFEErrCode 0.1:[ DDD-ERR ]ReadByKey (13) or ReadByCursor (0) != Expected (4100)
        if len(line) > 4 and line[3] == "DDD-ERR":
            ret_lines.append(line)

    return ret_lines

def count_unique_files(linelists):
    """
    count unique cut file 
    """
    n = 0
    has_seen = []
    for line in resultlines:
        #['./newck.output.cut-2826:', 'PFEErrCode', '12:', 'DDD-ERR', 'thr-10-txn-9', 'BEFORE', 'cut', 'not', 'committed']
        filename = line[0]
        if filename not in has_seen:
            has_seen.append(filename)
            n += 1
    return n




if __name__ == "__main__":

    fn = sys.argv[1] #all Err lines; each cut file may appear multiple times due to multiple Err in the file
    f = open(fn)
    resultlines = lines2lists(f)
    resultlines = get_DErr_lines(resultlines) #D err lines

    n_unique_DErr_files = count_unique_files(resultlines)


    TOT_CUTS = int(os.environ['TOT_CHECKED_CUTS']) 
    N_THR=int(os.environ['N_THR'])
    N_TXN_PER_THR=int(os.environ['N_TXN_PER_THR'])
    N_KEY_PER_TXN=int(os.environ['N_KEY_PER_TXN'])
    N_WORK_KEYS=int(os.environ['N_WORK_KEYS'])
    N_META_KEYS = N_THR * N_TXN_PER_THR
    N_TOT_KEYS = N_META_KEYS + N_WORK_KEYS #size of table, i.e. total row#

    n_rows = N_TOT_KEYS
    n_rows_per_txn = N_KEY_PER_TXN + 1; #plus a meta row

    tot_loss=0.0
    tot_txn_loss = 0.0
    tot_corrupt_loss = 0.0

    n_txn_loss_line = 0
    n_corrupt_loss_line = 0

    has_seen = []


    for line in resultlines:
        #['./newck.output.cut-2826:', 'PFEErrCode', '12:', 'DDD-ERR', 'thr-10-txn-9', 'BEFORE', 'cut', 'not', 'committed']

        #lost one txn: these are data lost on the readable rows
        #['./newck.output.cut-2826:', 'PFEErrCode', '12:', 'DDD-ERR', 'thr-10-txn-9', 'BEFORE', 'cut', 'not', 'committed']
        #could be multiple 12 errors for each cut
        if line[2] == "12:": 
            loss = float(n_rows_per_txn)/float(n_rows) #e.g., lost 1/10 rows in this cut
            tot_txn_loss += loss

            #could be multiple 12 errors for each cut
            filename = line[0]
            if filename not in has_seen:
                has_seen.append(filename)
                n_txn_loss_line += 1
    
        #lost partial table: these are data lost on unreadable rows
        #./newck.output.cut-2742:#PFEErrCode 0.1:[ DDD-ERR ]ReadByKey (13) or ReadByCursor (0) != Expected (4100)
        #at most one 0.1 error for each cut  
        if line[2] == "0.1:":
            byKey = float(line[5])
            byCursor = float(line[8])
            expected = float(line[-1])
            if byKey > byCursor or byCursor > expected: #sometimes byCursor may > expected
                loss=(expected - byKey) / expected #e.g., lost 5/10 rows in this cut
            else:
                loss=(expected - byCursor) / expected
            tot_corrupt_loss += loss  
            n_corrupt_loss_line += 1 

        #e.g. tot_loss in this cut is: 1/10 + 5/10 = 6/10
        #note: total data is 10 for this cut, no matter how many times it appear in the err log
        #so only count unique files to calculate total data

    tot_loss = tot_txn_loss + tot_corrupt_loss

    print "tot # of checked cuts: " + str(TOT_CUTS)
    print "tot # of cuts with D err: " + str(n_unique_DErr_files)
    print "tot # of cuts with txn loss D err: " + str(n_txn_loss_line)
    print "tot # of cuts with corrupt loss D err: " + str(n_corrupt_loss_line)

    if n_txn_loss_line != 0:
        avg_loss = tot_txn_loss/n_txn_loss_line
        print "Average txn Loss per cut (among all txn loss D-err-cuts) = " + str(avg_loss*100) + " %"
        avg_loss = tot_txn_loss/n_unique_DErr_files
        print "Average txn Loss per cut (among all D-err-cuts) = " + str(avg_loss*100) + " %"
        avg_loss = tot_txn_loss/TOT_CUTS
        print "Average txn loss per cut (among all cuts) = " + str(avg_loss*100) + " %"


    if n_corrupt_loss_line != 0:
        avg_loss = tot_corrupt_loss/n_corrupt_loss_line
        print "Average corrupt Loss per cut (among all corrupt loss D-err-cuts) = " + str(avg_loss*100) + " %"
        avg_loss = tot_corrupt_loss/n_unique_DErr_files
        print "Average corrupt Loss per cut (among all D-err-cuts) = " + str(avg_loss*100) + " %"
        avg_loss = tot_corrupt_loss/TOT_CUTS
        print "Average currupt loss per cut (among all cuts) = " + str(avg_loss*100) + " %"


    avg_loss = tot_loss/n_unique_DErr_files
    print "Average Loss per cut (among all D-err-cuts) = " + str(avg_loss*100) + " %"
    avg_loss = tot_loss/TOT_CUTS
    print "Average Loss per cut (among all cuts) = " + str(avg_loss*100) + " %"



 

