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

def getCommitLines(linelists):
    """get commit line and convert the ts to epoch"""
    ret_lines = [] 
    #SQLite special handling
    dotTS_dbs = ['OracleXE','MySQL', 'MariaDB', 'SQLServer']
    epoch_dbs = ['BDB', 'TC'] 
    TEST_DB_NAME = os.environ['TEST_DB_NAME']

    if TEST_DB_NAME in dotTS_dbs: 
        for line in linelists:
            if len(line) == 2:
                if 'meta' in line[0] and '2013' in line[1]:
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
            if len(line) == 2 and 'meta' in line[0]:
                #print line
                ts = int(float(line[1])*1000000)
                line[-1] = str(ts) 
                ret_lines.append(line)
                #print line
    return ret_lines

#def getCommitLines_bdb(linelists):
#    """get commit lines from bdb work log """
#    ret_lines = [] 
#    for line in linelists:
#        if len(line) == 2:
#            if 'meta' in line[0]:
#                ret_lines.append(line)
#    return ret_lines



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

    return ret_lines


def appendCommitToIO(commitlists, iolists):
    """append commit to io according to ts;
      all txn commited before the io are appended after the io"""
    ret_lines = []
    for ioline in iolists:
    #['IO', '1147', '1372179955058478']
        io_ts = ioline[2]
        for commitline in commitlists:
        #['k-98-meta-thr-10-txn-8', '1372179933094104']
            commit_ts = commitline[1] 
            if commit_ts <= io_ts:
                ioline.append(commitline[0])
                #ioline.append(commitline[1])
            else:
                break #commit_ts are in increasing order, no need to check following commitline
        ret_lines.append(ioline)
            
    return ret_lines
        

################################################################################
if __name__ == "__main__":

    worklog_fn = sys.argv[1]
    worklog_f = open(worklog_fn)
    resultlines = lines2lists(worklog_f)
    #for line in resultlines:
    #    print line
    commitlists = getCommitLines(resultlines)

    io_fn = sys.argv[2]
    io_f = open(io_fn)
    resultlines = lines2lists(io_f)
    iolists = getIOLines(resultlines)

    resultlines = appendCommitToIO(commitlists, iolists)

    for line in resultlines:
        print ' '.join(line)
