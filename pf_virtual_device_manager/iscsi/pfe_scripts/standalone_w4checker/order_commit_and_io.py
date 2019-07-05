#!/usr/bin/env python

import sys
import re
import fileinput
import os
import time
import datetime
import calendar
from check_wkld4 import lines2lists 
from check_wkld4 import convertTS 

TEST_DB_NAME = os.environ['TEST_DB_NAME']

def getCommitLines(linelists): #log.app-work contains ts after each commit
    """get commit line and convert the ts to epoch
       the ts is the upper bound of the commit (right after commit)
    """
    ret_lines = [] 
    #dotTS_dbs = ['OracleXE','MySQL', 'MariaDB', 'SQLServer']
    #k-9-meta-thr-1-txn-9    2014.03.15.22.37.29.943319
    dotTS_dbs = ['OracleXE','MySQL', 'MariaDB'] #SQLServer different

    epoch_dbs = ['BDB', 'TC', 'LMDB']

    TEST_DB_NAME = os.environ['TEST_DB_NAME']

    if TEST_DB_NAME in dotTS_dbs: 
    #k-9-meta-thr-1-txn-9    2014.03.15.22.37.29.943319
        for line in linelists:
            if len(line) == 2:
                #if 'meta' in line[0] and '2013' in line[1]:
                if 'meta' in line[0]: #year could be 2014, ... 
                    #print line
                    epoch_ts = convertTS(line[1])
                    line[1] = str(epoch_ts) #str consistent w/ other fileds
                    ret_lines.append(line)

    elif TEST_DB_NAME in epoch_dbs:
        for line in linelists:
            if len(line) == 2 and 'meta' in line[0]:
                ret_lines.append(line)

    elif TEST_DB_NAME == 'SQLite':
        for line in linelists:
            #['k-2-meta-thr-1-txn-2', '1373762063.24401']
            if len(line) >= 2 and 'meta' in line[0]:
                #print line
                ts = int(float(line[1])*1000000)
                line[-1] = str(ts) 
                ret_lines.append(line)
                #print line

    elif TEST_DB_NAME == 'SQLServer':
#        #PowerShell format:
#        #['keystr', ':', 'k-19-meta-thr-2-txn-9']
#        #['Column1', ':', '2014.03.30.17.44.01.417857']
#        key_str = ''
#        ts_str = ''
#        for line in linelists:
#            if len(line) == 3 and line[0] == 'keystr':
#                key_str = line[2]
#            if len(line) == 3 and line[0] == 'Column1':
#                ts_str = line[2]
#                epoch_ts = convertTS(ts_str)
#                new_line = [key_str, str(epoch_ts)]
#                #print new_line
#                ret_lines.append(new_line)

        #cygwin format:
        #normally: "k-9-meta-thr-1-txn-9    2014.03.15.22.37.29.943319"
        #rarely: "k-8-meta-thr-1-txn-8    2014.04.06.18.06.41.190400  Changed database context to 'pfe_db'."
        for line in linelists:
            #if len(line) == 2:
            if len(line) >= 2:
                if 'meta' in line[0]: #
                    #print line
                    epoch_ts = convertTS(line[1])
                    line[1] = str(epoch_ts) #str consistent w/ other fileds
                    new_line = [line[0], line[1]] #avoid len == 3 and "Changed database ..."
                    ret_lines.append(new_line)


    return ret_lines

def getBeforeCommitLines_TC(linelists): #log.app-work contains ts before each commit
    ret_lines = [] 
    TEST_DB_NAME = os.environ['TEST_DB_NAME']
    if TEST_DB_NAME == 'TC':
        for line in linelists:
            if len(line) == 3 and 'meta' in line[0] and line[2] == 'beforecommit':
                ret_lines.append(line[0:-1])
    return ret_lines

def getCommitLowerbound(linelist): #log.app-check contains ts before each commit (in eac meta row)
    """ get commit lowerbound (right before commit) from w4 meta rows of log.app-check 
    """
    dotTS_dbs = ['OracleXE','MySQL','MariaDB', 'SQLServer']
    epoch_dbs = ['BDB', 'TC', 'LMDB']
    TEST_DB_NAME = os.environ['TEST_DB_NAME']
    ret_map = {}
    for line in linelist:
        if len(line) == 2 and 'meta' in line[0] and 'meta' in line[1]: #a meta row
            key = line[0]
            value = line[1]
            valuelist = line[1].split('-')
            raw_ts = valuelist[-1]
            if TEST_DB_NAME in dotTS_dbs: 
                epoch_ts = convertTS(raw_ts)
                ts = str(epoch_ts) #str consistent w/ other fileds
            elif TEST_DB_NAME in epoch_dbs:
                ts = raw_ts
            elif TEST_DB_NAME == 'SQLite':
                ts = str(int(float(raw_ts)*1000000))

            ret_map[key] = ts
            
    return ret_map

def getCommitBounds(upperbound_list, lowerbound_map):
    """txn lower_ts upper_ts"""
    ret_lines = [] 
    for line in upperbound_list:
        txn_id = line[0]
        if txn_id in lowerbound_map:
            lowerbound = lowerbound_map[txn_id]
            line.insert(1,lowerbound)
            ret_lines.append(line)

    return ret_lines 


def getIOLines(linelists):
    """get IO# and ts from io file"""
    ret_lines = [] 
    for line in linelists:
    #1372179912878122 IO# 9 1075900416 4096 01f581ff0000141451c213d751c9cdc751c9cdc700000000000101f5
        io_ts = line[0]
        io_n = line[2]
        newline = ['IO']
        newline.append(io_n)
        newline.append(io_ts)
        ret_lines.append(newline)
        #newline_str = '-'.join(newline)
        #ret_lines.append(newline_str)

    return ret_lines


def appendCommitToIO(iolists, commitbounds, io_and_before, io_and_parallel, io_and_after):
    """append commit to io according to ts;
      all txn commited before the io are appended after the io"""
    ret_lines = []
    for ioline in iolists:
        #['IO', '1147', '1372179955058478']
        io_ts = ioline[2]
        ioline_str = '-'.join(ioline)
        #new_line = [ioline_str, [], [], []]
        #1st []: store commits before this IO 
        #2nd []: store commits // with this IO
        #3rd []: store commits after this IO
        io_and_before.append(ioline_str)
        io_and_parallel.append(ioline_str)
        io_and_after.append(ioline_str)

        for commitline in commitbounds:
        #['k-2-meta-thr-1-txn-2', '1373843865314010', '1373843867076020']
            commit_lowerbound = commitline[1] 
            commit_upperbound = commitline[2]
            commit_str = '-'.join(commitline) #include ts
            #if TEST_DB_NAME == 'SQLite': #SQLite has 1 ~ 5 digit fractional precision
            #    commit_lowerbound = int(commit_lowerbound)/10
            #    commit_upperbound = int(commit_upperbound)/10
            #    io_ts = int(io_ts)/10

            if commit_upperbound < io_ts:
                #io_and_before.append(commit_str)
                io_and_before[-1] = io_and_before[-1] + ' ' + commit_str
            elif commit_lowerbound > io_ts:
                #io_and_after.append(commit_str)
                io_and_after[-1] = io_and_after[-1] + ' ' + commit_str
            else:
                #io_and_parallel.append(commit_str)
                io_and_parallel[-1] = io_and_parallel[-1] + ' ' + commit_str
                #break #commit_ts are in increasing order, no need to check following commitline
        #ret_lines.append(new_line)
            
    #return ret_lines
        

################################################################################
if __name__ == "__main__":
    
    #formatted.io.txt
    io_fn = sys.argv[1]
    io_f = open(io_fn)
    resultlines = lines2lists(io_f)
    iolists = getIOLines(resultlines)

    #log.app-work: after commit ts
    worklog_fn = sys.argv[2]
    worklog_f = open(worklog_fn)
    resultlines = lines2lists(worklog_f)
    commitlists = getCommitLines(resultlines)
    #for l in commitlists:
    #    print l

    #if TEST_DB_NAME == 'TC':
    #    beforeCommitlists = getBeforeCommitLines_TC(resultlists): #log.app-work contains ts before each commit
    #    print beforeCommitlists

    checklog_fn = sys.argv[3]
    checklog_f = open(checklog_fn)
    resultlines = lines2lists(checklog_f)
    lowerbounds = getCommitLowerbound(resultlines)
    #for k, v in lowerbounds.items():
    #    print k, v


    commitbounds = getCommitBounds(commitlists, lowerbounds)

    io_and_before = []
    io_and_parallel = []
    io_and_after = []
    appendCommitToIO(iolists, commitbounds, io_and_before, io_and_parallel, io_and_after)


    io_and_before_fn = sys.argv[4]
    io_and_parallel_fn = sys.argv[5]
    io_and_after_fn = sys.argv[6]
    txn_bounds_fn = sys.argv[7]

    with open(io_and_before_fn, 'w') as f:
        for line in io_and_before:
            f.write(line + '\n')
    with open(io_and_parallel_fn, 'w') as f:
        for line in io_and_parallel:
            f.write(line + '\n')
    with open(io_and_after_fn, 'w') as f:
        for line in io_and_after:
            f.write(line + '\n')

    with open(txn_bounds_fn, 'w') as f:
        for commitline in commitbounds: 
            #['k-2-meta-thr-1-txn-2', '1373843865314010', '1373843867076020']
            commit_str = ' '.join(commitline) #include ts
            f.write(commit_str + '\n')
