#!/usr/bin/env python

import sys
import re
import fileinput
import os
import time
import datetime
import calendar

N_THR = int(os.environ['N_THR'])
N_TXN_PER_THR = int(os.environ['N_TXN_PER_THR']) 
N_KEY_PER_TXN = int(os.environ['N_KEY_PER_TXN']) 
N_META_KEYS = int(os.environ['N_META_KEYS'])
N_WORK_KEYS = int(os.environ['N_WORK_KEYS'])
N_TOT_KEYS = int(os.environ['N_TOT_KEYS']) 
WORK_KEY_START = int(os.environ['WORK_KEY_START']) 
WORK_KEY_END = int(os.environ['WORK_KEY_END'])
TEST_DB_NAME = os.environ['TEST_DB_NAME']

########################################
# formatting helpers
########################################

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


def getUsefulLines(linelists):
    """get key/value pair lines read by key"""
    ret_lines = [] 
    TEST_DB_NAME = os.environ['TEST_DB_NAME']

    dbgroup1 = ['BDB', 'TC'] #each ByCursor line xxfollowed a "+++++" line
#    dbgroup2 = ['MySQL', 'OracleXE', 'SQLite'] #all ByCursor lines after one "======ByCUrsor====" line
    dbgroup2 = ['MySQL', 'OracleXE', 'SQLite','MariaDB', 'SQLServer'] #all ByCursor lines after one "======ByCUrsor====" line

    useful_line_begin = False
    for line in linelists:
        if TEST_DB_NAME == "SQLite" and useful_line_begin == True and len(line) == 2:
            vallist = line[1].split('-')
            if len(vallist) > 2 and vallist[-2] == 'ts': # a commited meta row
                vallist[-1] = str(int(float(vallist[-1]) * 1000000))
            line[-1] = '-'.join(vallist)
            ret_lines.append(line)
            continue

        if TEST_DB_NAME != "SQLite" and useful_line_begin == True and len(line) == 2:
            ret_lines.append(line)
            useful_line_begin = False
            continue

        if TEST_DB_NAME in dbgroup1 and len(line) == 2 and '------' in line[0] and '------' in line[1]: 
            useful_line_begin = True 
            continue


        if TEST_DB_NAME == "OracleXE" and len(line) == 2 and '------' in line[0] and '------' in line[1]: 
            useful_line_begin = True 
            continue

        if TEST_DB_NAME == "MySQL" and len(line) == 2 and 'keystr' in line[0] and 'valstr' in line[1]: #mysql
            useful_line_begin = True 
            continue

        if TEST_DB_NAME == "MariaDB" and len(line) == 2 and 'keystr' in line[0] and 'valstr' in line[1]: #mysql
            useful_line_begin = True 
            continue

        if TEST_DB_NAME == "SQLServer" and len(line) == 2 and 'keystr' in line[0] and 'valstr' in line[1]: #sql server
            useful_line_begin = True 

        if TEST_DB_NAME == "SQLite" and len(line) == 1 and 'ByKey' in line[0]: #following rows ar byKey
            useful_line_begin = True
            continue

        if TEST_DB_NAME in dbgroup2 and len(line) == 1 and 'ByCursor' in line[0]:#following rows are byCursor
            break

    return ret_lines

def getUsefulLinesByCursor(linelists):
    """get key/value pair lines read by cursor """
    ret_lines = [] 
    TEST_DB_NAME = os.environ['TEST_DB_NAME']

    dbgroup1 = ['BDB', 'TC']
    dbgroup2 = ['MySQL', 'OracleXE', 'SQLite', 'MariaDB', 'SQLServer']

    useful_line_begin = False
    byCursor_begin = False

    for line in linelists:

        if TEST_DB_NAME in dbgroup1 and len(line) == 2 and '++++++' in line[0] and '++++++' in line[1]: 
            useful_line_begin = True 
            continue
        if TEST_DB_NAME in dbgroup1 and useful_line_begin == True:
            ret_lines.append(line)
            useful_line_begin = False
            continue

        if TEST_DB_NAME in dbgroup2 and len(line) == 1 and 'ByCursor' in line[0]:#following rows are byCursor
            byCursor_begin = True
            continue
        if TEST_DB_NAME in dbgroup2 and byCursor_begin == True and len(line) == 2 and 'k-' in line[0] and 'v-' in line[1]: 
            ret_lines.append(line)
            continue


    return ret_lines




def convertDotTS(dot_ts):
    """convert dot ts to epoch ts"""
    #dot_ts = '2013.06.21.16.14.34.262072' #should be about: 1371856473950896
    #dot_ts = '2013.06.21.16.14.45.222041' #should be about: 1371856484887964
    #dot_ts = '2013.06.21.16.14.54.770976' #should be about: 1371856494413837
    try:
        ts = time.strptime(dot_ts, '%Y.%m.%d.%H.%M.%S.%f')
    except ValueError:
        return 0
    epoch_sec = time.mktime(ts)
    splitted_ts = dot_ts.split('.') 
    epoch_microsec = splitted_ts[-1]
    epoch_ts = int(epoch_sec)*1000000 + int(epoch_microsec)
    #print "ts: " + str(epoch_ts)
    return epoch_ts

def convertTS(str_ts):
    TEST_DB_NAME = os.environ['TEST_DB_NAME']
    dotTS_dbs = ['OracleXE','MySQL', 'MariaDB', 'SQLServer']
    epoch_dbs = ['BDB', 'TC', 'SQLite']
    if TEST_DB_NAME in dotTS_dbs: 
        epoch_ts = convertDotTS(str_ts);
    elif TEST_DB_NAME in epoch_dbs:
        int_ts = int(str_ts)
        #epoch value sould be within a reasonable range
        if (int_ts > 1371856494413837) and (int_ts < 2371856494413837):
            epoch_ts = int(str_ts)
        else:
            epoch_ts = 0
    return epoch_ts


def reduceTable(linelists):
    """(after pass1) reduce table:
        rm 'k-N' column, rm 'v' and convert TS in 2nd column"""
    ret_lines = []
    for line in linelists:
        vallist = line[1].split('-')
        if len(vallist) > 2 and vallist[2] == "meta": 
            epoch_ts = convertTS(vallist[-1])
            vallist[-1] = str(epoch_ts) #str consistent w/ other fileds
        vallist = vallist[1:] #rm 'v'
        ret_lines.append(vallist) 

    return ret_lines 

def repairTable(linelists):
    """some rows are corrupted (missing), insert dummy rows"""
    #['k-99', 'v-99-meta-t....1.17.52.54.393249']
    # missing rows
    #['k-330', 'v-330']

    ret_lines = []

    firstline = linelists[0]
    key = firstline[0].split('-')
    first_id = int(key[1])
    if first_id != 1:#missing rows at the beginning 
        for id in range(1, first_id):
            newline = []
            dummy_key = 'k-' + str(id) + '-dummy'
            dummy_val = 'v-' + str(id) + '-dummy'
            newline.append(dummy_key)
            newline.append(dummy_val)
            ret_lines.append(newline)

    for i in range(len(linelists)-1):
        thisline = linelists[i]
        nextline = linelists[i+1]

        ret_lines.append(thisline)

        key = thisline[0].split('-') 
        this_id = int(key[1]) 
        key = nextline[0].split('-') 
        next_id = int(key[1])

        id_gap = next_id - this_id
        if id_gap > 1: #inset dummy lines if gap > 1
            for id in range(this_id + 1, next_id):
                newline = []
                dummy_key = 'k-' + str(id) + '-dummy'
                dummy_val = 'v-' + str(id) + '-dummy'
                newline.append(dummy_key)
                newline.append(dummy_val)
                ret_lines.append(newline)

        last_id = next_id 

    ret_lines.append(linelists[-1])

    id_gap = N_TOT_KEYS - last_id
    if id_gap >= 1:
        for id in range(last_id + 1, N_TOT_KEYS + 1):
            newline = []
            dummy_key = 'k-' + str(id) + '-dummy'
            dummy_val = 'v-' + str(id) + '-dummy'
            newline.append(dummy_key)
            newline.append(dummy_val)
            ret_lines.append(newline)

    return ret_lines 


def getCutIONumber(strfn):
#'test.output.sqlplus_check.cut-731'
   listfn = strfn.split('-') 
   return int(listfn[-1])

########################################
# single row checker 
########################################

def checkMetaRow(keylist, vallist):
#['k', '1', 'meta', 'thr', '1', 'txn', '1']
#['v', '1', 'meta', 'thr', '1', 'txn', '1', 'k', '38', '85', 'ts', '2013.06.21.14.40.36.220391']
    isBad = False
    
    isOldMetaKey = False 
    if isOldMetaKey:
        if len(vallist) != (10 + N_KEY_PER_TXN):
            isBad = True
            return isBad #avoid invalid index access in the follows 
    else:
        if len(keylist) != 7 or len(vallist) != (10 + N_KEY_PER_TXN):
            isBad = True
            return isBad #avoid invalid index access in the follows 
        #check key texts
        if keylist[2] != "meta" or keylist[3] != "thr" or keylist[5] != "txn" or \
           keylist[4] != vallist[4] or keylist[6] != vallist[6]:
            isBad = True

    #check val texts
    if vallist[2] != "meta" or vallist[3] != "thr" or vallist[5] != "txn" or \
       vallist[7] != "k" or vallist[-2] != "ts":
        isBad = True

    #check thr# and txn# in range
    if not (vallist[4].isdigit() and 1 <= int(vallist[4]) <= N_THR and
            vallist[6].isdigit() and 1 <= int(vallist[6]) <= N_TXN_PER_THR):
        isBad = True
    #check k# in range
    for k in vallist[8:-2]:
        if not (k.isdigit() and WORK_KEY_START <= int(k) <= N_TOT_KEYS):
            isBad = True
    #check ts format 
    epoch_ts = convertTS(vallist[-1])
    if epoch_ts == 0:
        isBad = True

    return isBad 

def checkWorkRow(keylist, vallist):
#['k', '18']
#['v', '18', 'thr', '1', 'txn', '2', 'k', '18']
    isBad = False
    if len(keylist) != 2 or len(vallist) != 8:
        isBad = True
        return isBad 
    if vallist[2] != "thr" or vallist[4] != "txn" or \
       vallist[6] != "k":
        isBad = True
    if not (vallist[3].isdigit() and 1 <= int(vallist[3]) <= N_THR and
            vallist[5].isdigit() and 1 <= int(vallist[5]) <= N_TXN_PER_THR and
            vallist[7].isdigit() and WORK_KEY_START <= int(vallist[7]) <= N_TOT_KEYS ):
        isBad = True
    return isBad


def SingleRowChecker(linelists): #
    """ check each row (a key/value pair) individually """

    print "#====== SingleRowCheckerBegin:" 
    bad = 0
    for line in linelists:
        if len(line) != 2:
            bad += 1
            print "FailureDetected: ErrCode 1; not a key value pair:\n" + str(line)
            continue

        if "dummy" in line[1]: #skip dummy row
            continue

        keylist = line[0].split('-')
        vallist = line[1].split('-')

        #basic check: k N  matches  v N
        if len(keylist) < 2 or len(vallist) < 2 or \
            keylist[0] != 'k' or vallist[0] != 'v' or \
            keylist[1] != vallist[1]:
            bad += 1
            print "FailureDetected: ErrCode 2: incorrect k-N / v-N:\n" + str(line)
            continue

        if len(vallist) > 2:
            if vallist[2] == "meta": 
                isBad = checkMetaRow(keylist, vallist)  
            else:
                isBad = checkWorkRow(keylist, vallist)
            if isBad:
                bad += 1
                print "FailureDetected: ErrCode 3: incorrect keystr/valstr format:\n" + str(line)

    if bad == 0:
        isBad = False
        print "#====== SingleRowCheckerEnd: CheckingPASSED" 
    else:
        isBad = True
        print "#====== SingleRowCheckerEnd: CheckingFAILED: #of_bad_rows / total_#of_rows: " + str(bad) + " / " + str(N_TOT_KEYS)

    return isBad



########################################
# Meta region checker
########################################
#note: table has been reduced. only has one column
#metarow: ['1', 'meta', 'thr', '1', 'txn', '1', 'k', '1036', '112', '111', '321', '342', '698', '124', '638', '791', '803', 'ts', '1371862369293448']
#workrow: ['92', 'thr', '1', 'txn', '10', 'k', '1092']
#initrow: ['4']

def checkTxnInOrder(linelists):
    """input: reduced linelists
       check all txn in a thread are commited in order,
       ie. should never see an uncommitted txn between two committed txn"""
    foundOutOfOrder = False
    for tid in range(1, N_THR + 1):
        foundCommittedTxn = False
        foundUncommittedTxn = False 
        first_metarow_idx = (tid-1) * N_TXN_PER_THR
        for txn_id in range(1, N_TXN_PER_THR + 1):
            this_metarow_idx = first_metarow_idx + txn_id - 1;
            metarow = linelists[this_metarow_idx]
            if len(metarow) > 2: #dummy row len == 2
                if metarow[1] == "meta" and metarow[3] == str(tid) and metarow[5] == str(txn_id):
                    foundCommittedTxn = True
                    if foundUncommittedTxn == True:
                        isBad = True
                        print "FailureDetected: ErrCode 6: found committed txn after uncommitted txn:\n" + str(metarow)
                else:
                    print "FailureDetected: ErrCode 7: wrong tid# or txn# in meta row:\n" + str(metarow)
            else:
                #metadata haven't been written to this row; 
                print "thr-" + str(tid) + "-txn-" + str(txn_id) + " was not committed." 
                foundUncommittedTxn = True
    return foundOutOfOrder


def checkTxnInOrder_wCutInfo(linelists, beforeCut_txns_str):
    """input: reduced linelists
       beforeCut_txns_str contains txns before cut : 'k-71-meta-thr-8-txn-1 k-31-meta-thr-4-txn-1 ... ';
       check all txn in a thread are commited in order,
       ie. should never see an uncommitted txn between two committed txn"""
    isBad = False
    for tid in range(1, N_THR + 1):
        foundCommittedTxn = False
        foundUncommittedTxn = False 
        first_metarow_idx = (tid-1) * N_TXN_PER_THR
        for txn_id in range(1, N_TXN_PER_THR + 1):
            txn_phrase = 'thr-' + str(tid) + '-txn-' + str(txn_id)
            this_metarow_idx = first_metarow_idx + txn_id - 1;
            metarow = linelists[this_metarow_idx]
            if (len(metarow) > 2) and (txn_phrase in beforeCut_txns_str): 
                if metarow[1] == "meta" and metarow[3] == str(tid) and metarow[5] == str(txn_id):
                    foundCommittedTxn = True
                    if foundUncommittedTxn == True:
                        isBad = True
                        print "FailureDetected: ErrCode 6: found committed txn after uncommitted txn:\n" + str(metarow)
                else:
                    print "FailureDetected: ErrCode 7: wrong tid# or txn# in meta row:\n" + str(metarow)
            elif txn_phrase in beforeCut_txns_str:
                #metadata haven't been written to this row; 
                print "FailureDetected: ErrCode 12: thr-" + str(tid) + "-txn-" + str(txn_id) + " was not committed. should had been commited." 
                isBad = True
                foundUncommittedTxn = True

            else:
                print "thr-" + str(tid) + "-txn-" + str(txn_id) + " was not committed." 
                foundUncommittedTxn = True

    return isBad


def checkAndAppendTSBound(linelists):
    """input: reduced linelists
       check the ts of txn in the same thr are in order,
       append the next txn's ts as this txn's upper bound ts"""
    isBad = False

    ts_idx = 8 + N_KEY_PER_TXN
    #check ts order and append ts bounds for each meta txn line
    for i in range(N_META_KEYS-1):
        thisline = linelists[i]
        nextline = linelists[i+1]

        if len(thisline) > 2 and len(nextline) > 2 and\
           thisline[1] == "meta" and nextline[1] == "meta" and\
           thisline[3] == nextline[3]:
            if int(thisline[ts_idx]) > int(nextline[ts_idx]):
                print "FailureDetected: ErrCode 8: meta row ts out of order:\n" + str(thisline) + "\n" + str(nextline) 
                isBad = True
            else:
                linelists[i].append('UB')
                linelists[i].append(nextline[ts_idx])

        if len(thisline) > 2 and len(nextline) > 2 and\
           thisline[1] == "meta" and nextline[1] == "meta" and\
           thisline[3] != nextline[3]: #next line is another thr's meta 
            linelists[i].append('fakeUB')
            linelists[i].append('9000000000000000')

        if i == N_META_KEYS - 2: #i+1 is the last thread's last txn
            linelists[i+1].append('fakeUB')
            linelists[i+1].append('9000000000000000')

        if len(thisline) > 2 and len(nextline) <= 2 and\
                thisline[1] == "meta":
            linelists[i].append('fakeUB')
            linelists[i].append('9000000000000000')


    return isBad


def MetaRegionChecker(linelists, beforeCut_txns_str):
    """input: reduced linelists
       beforeCut_txns_str contains txns before cut : 'k-71-meta-thr-8-txn-1 k-31-meta-thr-4-txn-1 ... ';
       check meta rows"""

    print "#====== MetaRegionCheckerBegin:"
    isMetaRowsFailed = False
    for idx, line in enumerate(linelists):
        #len(init_row) = 1, len(dummy_row) == 2
        if len(line) > 2 and line[1] == "meta":
            #a meta row must be within in N_META_KEYS
            if idx > (N_META_KEYS - 1): #-1: idx count from 0
                print "FailureDetected: ErrCode 4: meta row out of meta region:\n row#: " + str(idx) + ", " + str(line)
                isMetaRowsFailed = True
        
        if len(line) > 2 and line[1] != "meta":
                #a work txn row must be in work keys region
                if not (WORK_KEY_START-1 <= idx < WORK_KEY_END):
                    print "FailureDetected: ErrCode 5: work row in meta region:\n row#: " + str(idx) + ", " + str(line)
                    isMetaRowsFailed = True
    

    #isTxnBad = checkTxnInOrder(linelists)
    isTxnBad = checkTxnInOrder_wCutInfo(linelists, beforeCut_txns_str)
    isTSBad = checkAndAppendTSBound(linelists)

    isMetaRowsFailed = isMetaRowsFailed or isTxnBad or isTSBad
    
    if isMetaRowsFailed:
        print "#====== MetaRegionCheckerEnd: CheckingFAILED"
    else:
        print "#====== MetaRegionCheckerEnd: CheckingPASSED"

    return isMetaRowsFailed


########################################
# Transaction Commit checker
########################################
#metarow: ['2', 'meta', 'thr', '1', 'txn', '2', 'k', '731', '334', '588', '431', '1043', '519', '729', '277', '908', '468', 'ts', '1371862369809630', 'UB', '1371862370177262']
#workrow: ['92', 'thr', '1', 'txn', '10', 'k', '92']
#initrow: ['4']
#dummyrow: ['4', 'dummy']

def checkWorkKInMetaRow(linelists):
    """check each work row appear in some meta row"""
    isBad = False
    for work_k in range(WORK_KEY_START-1, WORK_KEY_END):
        workline = linelists[work_k]
        if len(workline) == 7: #not an init row or dummy row
            thr_id = int(workline[2])
            txn_id = int(workline[4])
            k_id = workline[-1]
            meta_k = (thr_id - 1) * N_TXN_PER_THR + (txn_id - 1)  
            metaline = linelists[meta_k]
            meta_k_id_set = metaline[7: 7+N_KEY_PER_TXN] 
            if k_id not in meta_k_id_set:
                print "FailureDetected: ErrCode 9: work k " + k_id + " does not exist in meta row:\n" +  str(workline) + "\n" + str(metaline)
                isBad = True
    return isBad


def checkWorkKInMetaRow_wCutInfo(linelists, beforeCut_txns_str):
    """beforeCut_txns_str contains txns before cut : 'k-71-meta-thr-8-txn-1 k-31-meta-thr-4-txn-1 ... ';
       if a work row belongs to a txn in the txn str, then:
            check each work row appear in some meta row, """
    isBad = False
    for work_k in range(WORK_KEY_START-1, WORK_KEY_END):
#        print work_k
        workline = linelists[work_k]
        if len(workline) == 7: #a work row
            thr_id = int(workline[2])
            txn_id = int(workline[4])
            k_id = workline[-1]
            meta_k = (thr_id - 1) * N_TXN_PER_THR + (txn_id - 1)  
            metaline = linelists[meta_k]
            txn_phrase = 'thr-' + str(thr_id) + '-txn-' + str(txn_id)
            #if (len(metaline) == 11+N_KEY_PER_TXN): 
            if (len(metaline) > 7+N_KEY_PER_TXN): 
                meta_k_id_set = metaline[7: 7+N_KEY_PER_TXN] 
                if k_id not in meta_k_id_set:
                    if txn_phrase in beforeCut_txns_str: 
                        print "FailureDetected: ErrCode 9.1: work k " + k_id + " (commited BEFORE cut) does not exist in meta row:\n" +  str(workline) + "\n" + str(metaline)
                    else:
                        print "FailureDetected: ErrCode 9.2: work k " + k_id + " (commited after cut) does not exist in meta row:\n" +  str(workline) + "\n" + str(metaline)
                        print "io_ts = " + io_ts
                        print "time gap: " + str(int(metaline[-1]) - int(io_ts)) 
                    isBad = True

            else: #not a  valid meta line
                #print str(len(metaline))
                #print str(11+N_KEY_PER_TXN)
                if txn_phrase in beforeCut_txns_str: 
                    print "FailureDetected: ErrCode 9.1: work k " + k_id + " (commited BEFORE cut) does not exist in meta row:\n" +  str(workline) + "\n" + str(metaline)
                else:
                    print "FailureDetected: ErrCode 9.2: work k " + k_id + " (commited after cut) does not exist in meta row:\n" +  str(workline) + "\n" + str(metaline)
                isBad = True

    return isBad


def checkMetaKInWorkRow(linelists):
    """check each k in meta row appear in work row, or overwritten by newer txn"""
    isBad = False
    for meta_row in range(N_META_KEYS):
        metaline = linelists[meta_row]
        if len(metaline) == 11+N_KEY_PER_TXN: #not an init row or dummy row
            meta_k_id_set = metaline[7: 7+N_KEY_PER_TXN]
            meta_thr_id = int(metaline[3])
            meta_txn_id = int(metaline[5])
            meta_ts_lowerbound = int(metaline[-3])
            #meta_ts_upperbound = int(metaline[-1])
            for k_id in meta_k_id_set:
                workline = linelists[int(k_id) - 1]
                if len(workline) < 7: 
                    print "FailureDetected: ErrCode 10: meta k " + k_id + " does not exist in work row:\n" +  str(metaline) + "\n" + str(workline)
                    isBad = True
                else:
                    work_thr_id = int(workline[2])
                    work_txn_id = int(workline[4])
                    if (work_thr_id != meta_thr_id) or (work_txn_id) != (meta_txn_id): #find other txn there
                        traceback_meta_row_id = (work_thr_id - 1) * N_TXN_PER_THR + (work_txn_id - 1)
                        traceback_metaline = linelists[traceback_meta_row_id]
                        #traceback_ts_lowerbound = int(traceback_metaline[-3])
                        traceback_ts_upperbound = int(traceback_metaline[-1])
                        if traceback_ts_upperbound < meta_ts_lowerbound:#there txn is an earlier commit
                            ts_delta = meta_ts_lowerbound - traceback_ts_upperbound
                            print "FailureDetected: ErrCode 11: k " + k_id + " overwritten by earlier txn! " + \
                                    str(ts_delta) + " microseconds out of order\n" +  str(metaline) + "\n" + str(workline) + "\n" + str(traceback_metaline)
                            isBad = True
    return isBad


def checkMetaKInWorkRow_wCutInfo(linelists, beforeCut_txns_str):
    """beforeCut_txns_str contains txns before cut : 'k-71-meta-thr-8-txn-1 k-31-meta-thr-4-txn-1 ... ';
      if a meta row belongs to a txn in beforeCut_txns_str, then
         check each k in the meta row appear in a work row, or overwritten by newer txn """
    isBad = False
    for meta_row in range(N_META_KEYS):
        metaline = linelists[meta_row]
        if len(metaline) == 11+N_KEY_PER_TXN: #a meta row
            meta_thr_id = metaline[3]
            meta_txn_id = metaline[5]

            txn_phrase = 'thr-' + meta_thr_id + '-txn-' + meta_txn_id

            meta_thr_id = int(meta_thr_id)
            meta_txn_id = int(meta_txn_id)

            meta_k_id_set = metaline[7: 7+N_KEY_PER_TXN]
            meta_ts_lowerbound = int(metaline[-3])
            for k_id in meta_k_id_set:
                workline = linelists[int(k_id) - 1]

                if len(workline) < 7: 
                    if txn_phrase in beforeCut_txns_str:
                        print "FailureDetected: ErrCode 10.1: meta k " + k_id + " (committed BEFORE cut) does not exist in work row:\n" +  str(metaline) + "\n" + str(workline)
                    else:
                        print "FailureDetected: ErrCode 10.2: meta k " + k_id + " (committed after cut) does not exist in work row:\n" +  str(metaline) + "\n" + str(workline)
                    isBad = True
                else:
                    work_thr_id = int(workline[2])
                    work_txn_id = int(workline[4])
                    if (work_thr_id != meta_thr_id) or (work_txn_id) != (meta_txn_id): #find other txn there
                        traceback_meta_row_id = (work_thr_id - 1) * N_TXN_PER_THR + (work_txn_id - 1)
                        traceback_metaline = linelists[traceback_meta_row_id]
                        traceback_ts_upperbound = int(traceback_metaline[-1])
                        if traceback_ts_upperbound < meta_ts_lowerbound:#there txn is an earlier commit
                            ts_delta = meta_ts_lowerbound - traceback_ts_upperbound

                            if txn_phrase in beforeCut_txns_str:
                                print "FailureDetected: ErrCode 11.1: k " + k_id + " (committed BEFORE cut) overwritten by earlier txn! " + \
                                        str(ts_delta) + " microseconds out of order\n" +  str(metaline) + "\n" + str(workline) + "\n" + str(traceback_metaline)
                            else:
                                print "FailureDetected: ErrCode 11.2: k " + k_id + " (committed after cut)  overwritten by earlier txn! " + \
                                        str(ts_delta) + " microseconds out of order\n" +  str(metaline) + "\n" + str(workline) + "\n" + str(traceback_metaline)
                            isBad = True

    return isBad


def TxnCommitChecker(linelists, beforeCut_txns_str):

    print "#====== TxnCommitCheckerBegin:"
    isTxnCommitFailed = False

    #isWorkKNotInMetaRow = checkWorkKInMetaRow(linelists)
    isWorkKNotInMetaRow = checkWorkKInMetaRow_wCutInfo(linelists, beforeCut_txns_str)
    #isMetaKNotInWorkRow = checkMetaKInWorkRow(linelists)
    isMetaKNotInWorkRow = checkMetaKInWorkRow_wCutInfo(linelists, beforeCut_txns_str)
    
    isTxnCommitFailed = isWorkKNotInMetaRow or isMetaKNotInWorkRow

    if isTxnCommitFailed:
        print "#====== TxnCommitCheckerEnd: CheckingFAILED"
    else:
        print "#====== TxnCommitCheckerEnd: CheckingPASSED"

    return isTxnCommitFailed


################################################################################
if __name__ == "__main__":


    print "TEST_DB_NAME = " + TEST_DB_NAME
    print "N_THR = " + str(N_THR)
    print "N_TXN_PER_THR = " + str(N_TXN_PER_THR)
    print "N_KEY_PER_TXN = " + str(N_KEY_PER_TXN) 
    print "N_META_KEYS = " + str(N_META_KEYS)
    print "N_WORK_KEYS = " + str(N_WORK_KEYS)
    print "N_TOT_KEYS = " + str(N_TOT_KEYS)
    print "WORK_KEY_START = " + str(WORK_KEY_START)
    print "WORK_KEY_END = " + str(WORK_KEY_END)

    fn = sys.argv[1]
    f = open(fn)
    io_and_commit_lines = lines2lists(f)
    #for line in io_and_commit_lines:
    #    print line
    #['IO', '445', '1372179931350776', 'k-71-meta-thr-8-txn-1', 'k-31-meta-thr-4-txn-1', ..., 'k-41-meta-thr-5-txn-1']

    for fn in sys.argv[2:]:
        print str(fn)
        cut_io_num = getCutIONumber(str(fn))
        print "CUT_IO_NUM = " + str(cut_io_num)
        io_line = io_and_commit_lines[cut_io_num - 1] 
        io_ts = io_line[2]
        beforeCut_txns_list = io_line[3:]
        beforeCut_txns_str = ' '.join(beforeCut_txns_list)
        #print "io_txns: " + beforeCut_txns_str
        n_txns_committed = len(beforeCut_txns_list)

        f = open(fn)
        lines = lines2lists(f)
        #for line in lines:
        #    print line
        resultlines = getUsefulLines(lines)
        #print "usefullinesByKey"
        #for line in resultlines:
        #    print line

        resultlinesByCursor = getUsefulLinesByCursor(lines)
        #print "usefullinesByCursor"
        #for line in resultlinesByCursor:
        #    print line

        

        print "#====== TableSizeCheckerBegin:"
        n_lines = len(resultlines)
        n_linesByCursor = len(resultlinesByCursor)
        if n_lines !=  n_linesByCursor:
            print "FailureDetected: ErrCode 0.0: (ReadableByKey " + str(n_lines) + ") != (ReadByCursor " + str(n_linesByCursor) + ")"
        else:
            print "(ReadableByKey " + str(n_lines) + ") == (ReadByCursor " + str(n_linesByCursor) + ")"
        if n_lines != N_TOT_KEYS:
            print "FailureDetected: ErrCode 0.1: Bad Table. readable rows = " + str(n_lines) + ", expected = " + str(N_TOT_KEYS) + \
                    ". # txns should had been committed = " + str(n_txns_committed) 
            if n_lines == 0:
                print "0 readable. skip this file."
                print "#====== TableSizeCheckerEnd: CheckingFAILED"

                continue
            else:
                resultlines = repairTable(resultlines)
                print "Table repaired."
                print "#====== TableSizeCheckerEnd: CheckingFAILED"
            #for line in resultlines:
            #    print line

            #continue
        else:
            print "#====== TableSizeCheckerEnd: CheckingPASSED"


        #for line in resultlines:
        #    print line
        isSingleRowCheckFailed = SingleRowChecker(resultlines)
        if isSingleRowCheckFailed:
            print "Single Row Check Failed. skip following checks."
            continue
    
        resultlines = reduceTable(resultlines)
        print "Table reduced."
        #for line in resultlines:
        #    print line

        isMetaRegionCheckFailed = MetaRegionChecker(resultlines, beforeCut_txns_str)
        #if isMetaRegionCheckFailed:
        #    print "Meta Region Check Failed. skip following check."
        #    continue
        #for line in resultlines:
        #    print line

        isTxnCommitCheckFailed = TxnCommitChecker(resultlines, beforeCut_txns_str) 


