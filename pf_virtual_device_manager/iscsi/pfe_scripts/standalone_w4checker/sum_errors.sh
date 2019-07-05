#!/usr/bin/env bash

absme=`readlink -f $0`
abshere=`dirname $absme`

#put all w4 logs in one maine dir
#LOGS_MAIN_DIR=$1

#for directory in $LOGS_MAIN_DIR/logs-*; do


    directory=$1
    #process one w4 log dir

    dir_basename=${directory##*/}
    
    PFE_LOG_DIR=$directory
    TESTFILE_DIR=$PFE_LOG_DIR
    RESULT_FILE=$PFE_LOG_DIR/summary_ACID.txt #each log dir has a summary


    #for all cuts in this dir
    cut_cnt=0
    tot_a_cnt=0
    tot_c_cnt=0
    tot_i_cnt=0
    tot_d_cnt=0

    for file in $TESTFILE_DIR/newck.output*; do
        #result file for one cut
        let "cut_cnt += 1"

        a_cnt=`grep AAA-ERR $file | wc -l`
        c_cnt=`grep CCC-ERR $file | wc -l`
        i_cnt=`grep III-ERR $file | wc -l`
        d_cnt=`grep DDD-ERR $file | wc -l`

        #only count once for each type of error in one result file
        if [ $a_cnt -gt 0 ]; then
            let "tot_a_cnt += 1"
        fi

        if [ $c_cnt -gt 0 ]; then
            let "tot_c_cnt += 1"
        fi
            
        if [ $i_cnt -gt 0 ]; then
            let "tot_i_cnt += 1"
        fi
            
        if [ $d_cnt -gt 0 ]; then
            let "tot_d_cnt += 1"
        fi
    done
    a_ratio=$(echo "$tot_a_cnt / $cut_cnt" | bc -l)
    c_ratio=$(echo "$tot_c_cnt / $cut_cnt" | bc -l)
    i_ratio=$(echo "$tot_i_cnt / $cut_cnt" | bc -l)
    d_ratio=$(echo "$tot_d_cnt / $cut_cnt" | bc -l)

    #save result for this log dir
    echo "TOTAL # of CUTS: $cut_cnt" | tee  $RESULT_FILE
    echo "AAA-ERR: $tot_a_cnt, $a_ratio" | tee -a  $RESULT_FILE
    echo "CCC-ERR: $tot_c_cnt, $c_ratio" | tee -a  $RESULT_FILE
    echo "III-ERR: $tot_i_cnt, $i_ratio" | tee -a  $RESULT_FILE
    echo "DDD-ERR: $tot_d_cnt, $d_ratio" | tee -a  $RESULT_FILE

#done
