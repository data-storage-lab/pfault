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
        line = line.rstrip() #rm carriage return 
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines


def getUsefulLines(linelists):
    """get key/value pair lines read by key"""
    ret_lines = [] 
    TEST_DB_NAME = os.environ['TEST_DB_NAME']

    dbgroup1 = ['BDB', 'TC', 'LMDB'] #each bykey row follows a "-------- --------" line, each byCursor row follows a "++++++++ ++++++" line
    #  19 ----------        ----------
    #  20 k-10-meta-thr-1-txn-10  v-10
    #  21 ----------        ----------
    #  22 k-11  v-11
    #  23 ----------        ----------
    #  24 k-12  v-12

    dbgroup2 = ['MySQL', 'MariaDB', 'OracleXE', 'SQLite'] #'SQLServer' in diff func; #all Bykey lines before the "==================ByCUrsor====" line

    useful_line_begin = False
    for line in linelists:

        if TEST_DB_NAME == "SQLite" and useful_line_begin == True and len(line) == 2:
            vallist = line[1].split('-')
            if len(vallist) > 2 and vallist[-2] == 'ts': # a commited meta row
                vallist[-1] = str(int(float(vallist[-1]) * 1000000))
            line[-1] = '-'.join(vallist)
            ret_lines.append(line)
            continue

        if TEST_DB_NAME != "SQLite" and useful_line_begin == True and len(line) == 2 and 'k-' in line[0] and 'v-' in line[1]:
            ret_lines.append(line)
            useful_line_begin = False
            continue

        if TEST_DB_NAME in dbgroup1 and len(line) == 2 and '------' in line[0] and '------' in line[1]: 
            useful_line_begin = True 
            continue


        if TEST_DB_NAME == "OracleXE" and len(line) == 2 and '------' in line[0] and '------' in line[1]: 
            useful_line_begin = True 
            continue

        if TEST_DB_NAME in dbgroup2 and TEST_DB_NAME != "OracleXE" and len(line) == 2 and 'keystr' in line[0] and 'valstr' in line[1]: #mysql, mariadb
            useful_line_begin = True 
            continue

        if TEST_DB_NAME == "SQLite" and len(line) == 1 and 'ByKey' in line[0]: #following rows ar byKey
            useful_line_begin = True
            continue

        if TEST_DB_NAME in dbgroup2 and len(line) == 1 and 'ByCursor' in line[0]:#following rows are byCursor
            break

    return ret_lines

def getUsefulLinesByKey_SQLServer(linelists):
    """get key/value pair lines read by key"""
    ret_lines = [] 
    TEST_DB_NAME = os.environ['TEST_DB_NAME']

    for line in linelists:
        if len(line) == 2 and 'k-' in line[0] and 'v-' in line[1]:
            ret_lines.append(line)
            continue

        if len(line) == 1 and 'ByCursor' in line[0]:#following rows are byCursor
            break

    return ret_lines



def getUsefulLinesByCursor(linelists):
    """get key/value pair lines read by cursor """
    ret_lines = [] 
    TEST_DB_NAME = os.environ['TEST_DB_NAME']

    dbgroup1 = ['BDB', 'TC', 'LMDB']
    dbgroup2 = ['MySQL', 'MariaDB','OracleXE', 'SQLite', 'SQLServer']

    useful_line_begin = False
    byCursor_begin = False

    for line in linelists:

        #dbgroup1 ByCursor format: no "ByCursor" line, each row separated by "++++++++ ++++++++"
        #2023 +++++++++++     +++++++++++
        #2024 k-10-meta-thr-1-txn-10  v-10
        #2025 +++++++++++     +++++++++++
        #2026 k-100  v-100
        #2027 +++++++++++     +++++++++++
        #2028 k-1000  v-1000

        
        if TEST_DB_NAME in dbgroup1 and len(line) == 2 and '++++++' in line[0] and '++++++' in line[1]: 
            useful_line_begin = True 
            continue
        if TEST_DB_NAME in dbgroup1 and useful_line_begin == True:
            ret_lines.append(line)
            useful_line_begin = False
            continue

        #dbgroup2 ByCursor format: has one "ByCursor" line, followed by all rows (no separator between rows)
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
    epoch_dbs = ['BDB', 'TC', 'SQLite', 'LMDB']
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

    print "#================== SingleRowCheckerBegin:" 
    bad = 0
    for line in linelists:
        if len(line) != 2:
            bad += 1
            print "#PFEErrCode 1:" + C_ERR + D_ERR + "len != 2, not a key/value pair" 
            print str(line)
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
            print "#PFEErrCode 2:" + C_ERR + "wrong 'k' 'N' 'v' 'N' format"
            print str(line)
            continue

        if len(vallist) > 2:
            if vallist[2] == "meta": 
                isBad = checkMetaRow(keylist, vallist)  
            else:
                isBad = checkWorkRow(keylist, vallist)
            if isBad:
                bad += 1
                print "#PFEErrCode 3:" + C_ERR + "wrong keystr/valstr format"
                print str(line)

    if bad == 0:
        isBad = False
        print "#================== SingleRowCheckerEnd: CheckingPASSED" 
    else:
        isBad = True
        print "#================== SingleRowCheckerEnd: CheckingFAILED: #of_bad_rows / total_#of_rows: " + str(bad) + " / " + str(N_TOT_KEYS)

    return isBad



########################################
# Meta region checker
########################################
#note: table has been reduced. only has one column
#metarow: ['1', 'meta', 'thr', '1', 'txn', '1', 'k', '1036', '112', '111', '321', '342', '698', '124', '638', '791', '803', 'ts', '1371862369293448']
#workrow: ['92', 'thr', '1', 'txn', '10', 'k', '1092']
#initrow: ['4']

def checkTxnInOrder_wCutInfo(linelists, beforeCut_txns_str, afterCut_txns_str , txn_bounds_map):
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
            if (len(metarow) > 2) and (txn_phrase in beforeCut_txns_str): # > 2 means not a dummy row 
                if metarow[1] == "meta" and metarow[3] == str(tid) and metarow[5] == str(txn_id):
                    foundCommittedTxn = True
                    if foundUncommittedTxn == True:
                        isBad = True
                        if TEST_DB_NAME == "OracleXE":
                            print "#PFEErrCode 6: committed txn (BEFORE cut) after uncommitted txn! (could because OracleXE abort) "
                        else:
                            print "#PFEErrCode 6:" + D_ERR +"committed txn (BEFORE cut) after uncommitted txn!"
                        print str(lastUncommittedTxn)
                        print str(metarow)
                        print io_info
                        print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
                else:
                    print "#PFEErrCode 7:" + C_ERR + "wrong tid# or txn# in meta row"
                    print str(metarow)
                    print io_info
                    print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
            elif txn_phrase in beforeCut_txns_str:
                #metadata haven't been written to this row; 
                print "#PFEErrCode 12:"+ D_ERR + txn_phrase + " (BEFORE cut) not committed!"
                print str(metarow)
                print io_info
                print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
                isBad = True
                foundUncommittedTxn = True
                lastUncommittedTxn = metarow 

            else: #init or dummy rows, and the txn is not before cut
                print "thr-" + str(tid) + "-txn-" + str(txn_id) + " was not committed." 
                foundUncommittedTxn = True
                lastUncommittedTxn = metarow 

    return isBad

#deprecated
#def checkAndAppendTSBound(linelists):
#    """input: reduced linelists
#       check the ts of txn in the same thr are in order,
#       append the next txn's ts as this txn's upper bound ts"""
#    isBad = False
#    ts_idx = 8 + N_KEY_PER_TXN
#    #check ts order and append ts bounds for each meta txn line
#    for i in range(N_META_KEYS-1):
#        thisline = linelists[i]
#        nextline = linelists[i+1]
#
#        if len(thisline) > 2 and len(nextline) > 2 and\
#           thisline[1] == "meta" and nextline[1] == "meta" and\
#           thisline[3] == nextline[3]:
#            if int(thisline[ts_idx]) > int(nextline[ts_idx]):
#                print "FailureDetected: ErrCode 8: meta row ts out of order:\n" + str(thisline) + "\n" + str(nextline) 
#                isBad = True
#            else:
#                linelists[i].append('UB')
#                linelists[i].append(nextline[ts_idx])
#
#        if len(thisline) > 2 and len(nextline) > 2 and\
#           thisline[1] == "meta" and nextline[1] == "meta" and\
#           thisline[3] != nextline[3]: #next line is another thr's meta 
#            linelists[i].append('fakeUB')
#            linelists[i].append('9000000000000000')
#
#        if i == N_META_KEYS - 2: #i+1 is the last thread's last txn
#            linelists[i+1].append('fakeUB')
#            linelists[i+1].append('9000000000000000')
#
#        if len(thisline) > 2 and len(nextline) <= 2 and\
#                thisline[1] == "meta":
#            linelists[i].append('fakeUB')
#            linelists[i].append('9000000000000000')
#    return isBad

def appendTSBound_and_checkTSOrder(linelists, txn_bounds_map):
    isBad = False
    for tid in range(1, N_THR + 1):
        first_metarow_idx = (tid-1) * N_TXN_PER_THR
        for txn_id in range(1, N_TXN_PER_THR + 1):
            txn_phrase = 'thr-' + str(tid) + '-txn-' + str(txn_id)
            metarow_idx = first_metarow_idx + txn_id - 1;
            metarow = linelists[metarow_idx]
            if len(metarow) > 2 and metarow[1] == "meta": #not init or dummy value
                bounds_str = txn_bounds_map[txn_phrase]
                bounds_list = bounds_str.split('-')
                upperbound = bounds_list[1]
                linelists[metarow_idx].append('UB') #maybe useless
                linelists[metarow_idx].append(upperbound)

    ts_idx = 8 + N_KEY_PER_TXN
    for i in range(N_META_KEYS-1):
        thisline = linelists[i]
        nextline = linelists[i+1]
        if len(thisline) > 2 and len(nextline) > 2 and\
           thisline[1] == "meta" and nextline[1] == "meta" and\
           thisline[3] == nextline[3]:
            if int(thisline[ts_idx]) > int(nextline[ts_idx]):
                print "#PFEErrCode 8:"+ C_ERR +"meta row ts out of order:\n" + str(thisline) + "\n" + str(nextline) 
                isBad = True
 
    return isBad

def MetaRegionChecker(linelists, beforeCut_txns_str, afterCut_txns_str , txn_bounds_map):
    """input: reduced linelists
       beforeCut_txns_str contains txns before cut : 'k-71-meta-thr-8-txn-1 k-31-meta-thr-4-txn-1 ... ';
       check meta rows"""

    print "#================== MetaRegionCheckerBegin:"
    isMetaRowsFailed = False
    for idx, line in enumerate(linelists):
        #len(init_row) = 1, len(dummy_row) == 2
        if len(line) > 2 and line[1] == "meta":
            #a meta row must be within in N_META_KEYS
            if idx > (N_META_KEYS - 1): #-1: idx count from 0
                print "#PFEErrCode 4:"+ C_ERR +"meta row out of meta region"
                print str(line)
                print "found at row#: " + str(idx)
                print "N_META_KEYS: " + N_META_KEYS
                isMetaRowsFailed = True
        
        if len(line) > 2 and line[1] != "meta":
                #a work txn row must be in work keys region
                if not (WORK_KEY_START-1 <= idx < WORK_KEY_END):
                    print "#PFEErrCode 5:"+ C_ERR +"work row in meta region"
                    print str(line)
                    print "found at row#: " + str(idx)
                    print "N_META_KEYS: " + N_META_KEYS
                    isMetaRowsFailed = True
    

    #isTxnBad = checkTxnInOrder(linelists)
    isTxnBad = checkTxnInOrder_wCutInfo(linelists, beforeCut_txns_str, afterCut_txns_str , txn_bounds_map)
#    isTSBad = checkAndAppendTSBound(linelists)
    isTSBad = appendTSBound_and_checkTSOrder(linelists, txn_bounds_map)

    isMetaRowsFailed = isMetaRowsFailed or isTxnBad or isTSBad
    
    if isMetaRowsFailed:
        print "#================== MetaRegionCheckerEnd: CheckingFAILED"
    else:
        print "#================== MetaRegionCheckerEnd: CheckingPASSED"

    return isMetaRowsFailed


########################################
# Transaction Commit checker
########################################
#metarow: ['2', 'meta', 'thr', '1', 'txn', '2', 'k', '731', '334', '588', '431', '1043', '519', '729', '277', '908', '468', 'ts', '1371862369809630', 'UB', '1371862370177262']
#workrow: ['92', 'thr', '1', 'txn', '10', 'k', '92']
#initrow: ['4']
#dummyrow: ['4', 'dummy']


def checkWorkKInMetaRow_wCutInfo(linelists, beforeCut_txns_str, afterCut_txns_str, txn_bounds_map):
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
            if (len(metaline) > 7+N_KEY_PER_TXN): #a valid meta line 
                meta_k_id_set = metaline[7: 7+N_KEY_PER_TXN] 
                if k_id not in meta_k_id_set:
                    if txn_phrase in beforeCut_txns_str: 
                        print "#PFEErrCode 9.1.1:" + A_ERR + D_ERR + "work k " + k_id + " (BEFORE cut) not in meta row; meta row valid"
                    elif txn_phrase in afterCut_txns_str:
                        print "#PFEErrCode 9.2.1:" + A_ERR + I_ERR + "work k " + k_id + " (after cut) not in meta row; meta row valid" 
                    else: #txn parallel w/ io, skip 
                        print "#PFEErrCode 9.3.1:" + A_ERR + "work k " + k_id + " (parallel with cut) not in meta row; meta row valid" 
                    print str(metaline)
                    print str(workline)
                    print io_info
                    print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
                    isBad = True

            elif len(metaline) == 1: #an initial line
                if txn_phrase in beforeCut_txns_str: 
                    print "#PFEErrCode 9.1.2:" + A_ERR + D_ERR + "work k " + k_id + " (BEFORE cut) not in meta row; meta row initial"
                elif txn_phrase in afterCut_txns_str:
                    print "#PFEErrCode 9.2.2:" + A_ERR + I_ERR + "work k " + k_id + " (after cut) not in meta row; meta row initial"
                else: #txn parallel w/ io, skip 
                    print "#PFEErrCode 9.3.2:" + A_ERR + "work k " + k_id + " (parallel with cut) not in meta row; meta row initial"
                print str(metaline)
                print str(workline)
                print io_info
                print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
                isBad = True
            elif len(metaline) == 2 and metaline[1] == "dummy": #a corrupted line
                if txn_phrase in beforeCut_txns_str: 
                    print "#PFEErrCode 9.1.3:" + D_ERR +"work k " + k_id + " (BEFORE cut) not in meta row; meta row corrupted"
                elif txn_phrase in afterCut_txns_str:
                    print "#PFEErrCode 9.2.3:" + I_ERR + D_ERR +"work k " + k_id + " (after cut) not in meta row; meta row corrupted"
                else: #txn parallel w/ io, skip 
                    print "#PFEErrCode 9.3.3:" + D_ERR +"work k " + k_id + " (parallel with cut) not in meta row; meta row corrupted"
                print str(metaline)
                print str(workline)
                print io_info
                print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
                isBad = True


    return isBad



def checkMetaKInWorkRow_wCutInfo(linelists, beforeCut_txns_str , afterCut_txns_str, txn_bounds_map):
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
                if len(workline) == 2 and workline[1] == "dummy": #a corruptted line 
                    if txn_phrase in beforeCut_txns_str:
                        print "#PFEErrCode 10.1.3:" + D_ERR +"meta k " + k_id + " (BEFORE cut) not in work row; work row corrupted"
                    elif txn_phrase in afterCut_txns_str:
                        print "#PFEErrCode 10.2.3:" + I_ERR + D_ERR +"meta k " + k_id + " (after cut) not in work row; work row corrupted"
                    else: #txn parallel w/ io, skip 
                        print "#PFEErrCode 10.3.3:" + D_ERR +"meta k " + k_id + " (parallel with cut) not in work row; work row corrupted"
                    print str(metaline)
                    print str(workline)
                    print io_info
                    print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
                    isBad = True
                elif len(workline) == 1: #a init line
                    if txn_phrase in beforeCut_txns_str:
                        print "#PFEErrCode 10.1.2:" + A_ERR + D_ERR + "meta k " + k_id + " (BEFORE cut) not in work row; work row initial"
                    elif txn_phrase in afterCut_txns_str:
                        print "#PFEErrCode 10.2.2:" + A_ERR + I_ERR + "meta k " + k_id + " (after cut) not in work row; work row initial"
                    else: #txn parallel w/ io, skip 
                        print "#PFEErrCode 10.3.2:" + A_ERR + "meta k " + k_id + " (parallel with cut) not in work row; work row initial"
                    print str(metaline)
                    print str(workline)
                    print io_info
                    print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
                    isBad = True

                elif len(workline) == 7: #a valid workline
                    work_thr_id = int(workline[2])
                    work_txn_id = int(workline[4])
                    if (work_thr_id != meta_thr_id) or (work_txn_id) != (meta_txn_id): #find other txn there
                        traceback_meta_row_id = (work_thr_id - 1) * N_TXN_PER_THR + (work_txn_id - 1)
                        traceback_metaline = linelists[traceback_meta_row_id]
                        traceback_ts_upperbound = int(traceback_metaline[-1])
                        if traceback_ts_upperbound < meta_ts_lowerbound:#there txn is from an earlier commit
                            ts_delta = meta_ts_lowerbound - traceback_ts_upperbound
                            if txn_phrase in beforeCut_txns_str:
                                print "#PFEErrCode 10.1.1:" + A_ERR + D_ERR + "meta k " + k_id + " (BEFORE cut) not in work row; work row overwritten by early txn."
                            elif txn_phrase in afterCut_txns_str:
                                print "#PFEErrCode 10.2.1:" + A_ERR + I_ERR + "meta k " + k_id + " (after cut) not in work row; work row overwritten by early txn." 
                            else: #txn parallel w/ io, skip 
                                print "#PFEErrCode 10.3.1:" + A_ERR + "meta k " + k_id + " (parallel cut) not in work row; work row overwritten by early txn." 
                            print str(ts_delta) + " microsecs out of order"
                            print str(metaline)
                            print str(workline)
                            print str(traceback_metaline)
                            print io_info
                            print txn_phrase + ' ' + txn_bounds_map[txn_phrase]
                            isBad = True

    return isBad


def TxnCommitChecker(linelists, beforeCut_txns_str, afterCut_txns_str, txn_bounds_map):

    print "#================== TxnCommitCheckerBegin:"
    isTxnCommitFailed = False

    isWorkKNotInMetaRow = checkWorkKInMetaRow_wCutInfo(linelists, beforeCut_txns_str, afterCut_txns_str, txn_bounds_map)
    isMetaKNotInWorkRow = checkMetaKInWorkRow_wCutInfo(linelists, beforeCut_txns_str, afterCut_txns_str, txn_bounds_map)
    
    isTxnCommitFailed = isWorkKNotInMetaRow or isMetaKNotInWorkRow

    if isTxnCommitFailed:
        print "#================== TxnCommitCheckerEnd: CheckingFAILED"
    else:
        print "#================== TxnCommitCheckerEnd: CheckingPASSED"

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

    A_ERR = "[ AAA-ERR ]"
    C_ERR = "[ CCC-ERR ]" 
    I_ERR = "[ III-ERR ]"
    D_ERR = "[ DDD-ERR ]"

    fn = sys.argv[1]
    f = open(fn)
    #io_and_commit_lines = lines2lists(f) #io and commits before the io
    io_and_before = lines2lists(f) #io and commits before the io
    #for line in io_and_before:
    #    print line
    #['IO-64-1373764104432564', 'k-1-meta-thr-1-txn-1-1373764101894990-1373764103166000', 'k-2-meta-thr-1-txn-2-1373764103167000-1373764104123990']


    fn = sys.argv[2]
    f = open(fn)
    io_and_parallel = lines2lists(f)

    #for line in io_and_parallel:
    #    print line
    #['IO-259-1373764113635680', 'k-10-meta-thr-1-txn-10-1373764112641990-1373764113856990']


    fn = sys.argv[3]
    f = open(fn)
    io_and_after = lines2lists(f)

    #for line in io_and_after:
    #    print line
    #['IO-209-1373764111197044', 'k-9-meta-thr-1-txn-9-1373764111267980-1373764112640980', 'k-10-meta-thr-1-txn-10-1373764112641990-1373764113856990']


    fn = sys.argv[4]
    f = open(fn)
    txn_bounds = lines2lists(f)
    #for line in txn_bounds:
    #    print line
    #['k-2-meta-thr-1-txn-2', '1373764103167000', '1373764104123990']
    txn_bounds_map = {}
    for line in txn_bounds:
        long_txn_id = line[0]
        bounds = line[1] + '-' + line[2]
        short_txn_id = long_txn_id.split('-')
        short_txn_id = '-'.join(short_txn_id[3:])
        #short_txn_id:  "thr-7-txn-1"
        txn_bounds_map[short_txn_id] = bounds
    
    #for k, v in txn_bounds_map.items():
    #    print k, ' : ', v 
    #"thr-7-txn-9  :  1374180363812706-1374180363887029"
  



    for fn in sys.argv[5:]:
        print str(fn)
        cut_io_num = getCutIONumber(str(fn))
        print "CUT_IO_NUM = " + str(cut_io_num)
        #io_line = io_and_commit_lines[cut_io_num - 1] 
        io_line = io_and_before[cut_io_num - 1] 
        io_info = io_line[0]
        beforeCut_txns_list = io_line[1:]
        beforeCut_txns_str = ' '.join(beforeCut_txns_list)

        io_line = io_and_after[cut_io_num - 1]
        #print "io_and_after_line " + str(io_line)
        afterCut_txns_list = io_line[1:]
        afterCut_txns_str = ' '.join(afterCut_txns_list)
        #print "aftercuttxnstr " + afterCut_txns_str

        f = open(fn)
        lines = lines2lists(f)

        TEST_DB_NAME = os.environ['TEST_DB_NAME']
        if TEST_DB_NAME != "SQLServer": 
            resultlines = getUsefulLines(lines)
        else:
            resultlines = getUsefulLinesByKey_SQLServer(lines)

        #print "usefullinesByKey"
        #for line in resultlines:
        #   print line

        resultlinesByCursor = getUsefulLinesByCursor(lines)
        #print "usefullinesByCursor"
        #for line in resultlinesByCursor:
         #   print line

        

        print "#================== TableSizeCheckerBegin:"
        isFail = False
        n_linesByKey = len(resultlines)
        n_linesByCursor = len(resultlinesByCursor)
        if n_linesByKey !=  n_linesByCursor:
            print "#PFEErrCode 0.0:" + C_ERR + "(ReadByKey " + str(n_linesByKey) + ") != (ReadByCursor " + str(n_linesByCursor) + ")"
            isFail = True
        else:
            print "(ReadByKey " + str(n_linesByKey) + ") == (ReadByCursor " + str(n_linesByCursor) + ")"
        if n_linesByCursor != N_TOT_KEYS and n_linesByKey != N_TOT_KEYS:
            print "#PFEErrCode 0.1:" + D_ERR + "ReadByKey (" + str(n_linesByKey) + ") or ReadByCursor (" + str(n_linesByCursor) + ") != Expected (" + str(N_TOT_KEYS) + ")"
            isFail = True
        else:
            print "(ReadByKey " + str(n_linesByKey) + ") == (ReadByCursor " + str(n_linesByCursor) + ") == (Expected "+ str(N_TOT_KEYS) + ")"

        if n_linesByKey != N_TOT_KEYS:
            isFail = True
            if n_linesByKey == 0:
                print "0 readable by ke. skip this file."
                print "#================== TableSizeCheckerEnd: CheckingFAILED"
                continue
            else:
                resultlines = repairTable(resultlines)
                print "Table repaired."

        if isFail:
            print "#================== TableSizeCheckerEnd: CheckingFAILED"
        else:
            print "#================== TableSizeCheckerEnd: CheckingPASSED"


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

        isMetaRegionCheckFailed = MetaRegionChecker(resultlines, beforeCut_txns_str, afterCut_txns_str, txn_bounds_map)
        #if isMetaRegionCheckFailed:
        #    print "Meta Region Check Failed. skip following check."
        #    continue
        #for line in resultlines:
        #    print line

        isTxnCommitCheckFailed = TxnCommitChecker(resultlines, beforeCut_txns_str, afterCut_txns_str, txn_bounds_map) 


