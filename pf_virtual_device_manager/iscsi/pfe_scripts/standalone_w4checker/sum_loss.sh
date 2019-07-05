#!/usr/bin/env bash

#./THISFILE /FULLPATH/LOG_DIR

absme=`readlink -f $0`
abshere=`dirname $absme`

#put all w4 logs in one dir
#LOGS_MAIN_DIR=$1

#for directory in $LOGS_MAIN_DIR/logs-*fail-0*; do

    directory=$1
    #process one w4 cleancut log dir

    dir_basename=${directory##*/}
    
    RESULT_FILE=$directory/summary_lossPercent.txt #each log dir has a percentage result
    TEMP_FILE=/tmp/tmpfile

    #newck.output.cut-2742:#PFEErrCode 0.1:[ DDD-ERR ]ReadByKey (13) or ReadByCursor (0) != Expected (4100)
    #pattern1=" 0.1:"   
    #newck.output.cut-103:#PFEErrCode 12:[ DDD-ERR ]thr-4-txn-2 (BEFORE cut) not committed!
    #pattern2=" 12:"

    #all Err lines
    pattern="Err"


    cd $directory
    TOT_CHECKED_CUTS=`ls newck.output* | wc -l` #only consider checked cuts
    export TOT_CHECKED_CUTS
    . w4_env_conf.sh #get txn size

    grep $pattern ./newck.output* > $TEMP_FILE #note: each file may appear multip times due to multipe Err in the file
    
    echo $dir_basename
    $abshere/count_loss.py $TEMP_FILE 2>&1 | tee $RESULT_FILE 
    cd -

#done
