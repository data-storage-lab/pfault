#!/usr/bin/env bash

#APP_DIR=./
TESTFILE_DIR=$PFE_LOG_DIR
#RESULT_FILE=$PFE_LOG_DIR/check_result.txt
#: > $RESULT_FILE 

COMMIT_FILE=$PFE_LOG_DIR/log.app-work
IO_FILE=$PFE_LOG_DIR/formatted.io.txt
IO_AND_COMMIT_FILE=$PFE_LOG_DIR/tmp.io_and_commits.txt

$PFE_SCRIPT_DIR/postproc/order_commit_and_io.py $COMMIT_FILE $IO_FILE > $IO_AND_COMMIT_FILE
echo $PY_CHECKER
#for file in $TESTFILE_DIR/output*; do
file=$1
    echo -e "\n################# Start processing $file" # >> $RESULT_FILE
    $PY_CHECKER $IO_AND_COMMIT_FILE $file # >> $RESULT_FILE 2>&1
    echo -e "###Done with $file\n" # >> $RESULT_FILE
#done
