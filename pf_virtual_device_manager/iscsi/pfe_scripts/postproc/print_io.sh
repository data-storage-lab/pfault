#!/usr/bin/env bash

#print the content of a range of IO
#usage:
#./THIS_FILE FIRST_PRINT_IO LAST_PRINT_IO PFE_LOG_DIR

FIRST_PRINT_IO=$1
LAST_PRINT_IO=$2
PFE_LOG_DIR=$3

IO_HEAD_FILE=$PFE_LOG_DIR/pfe_io_head_split_log.od
IO_DATA_FILE=$PFE_LOG_DIR/pfe_io_data_log.work.od

. $PFE_LOG_DIR/pfe_local.sh
PFE_LOG_DIR=$3 #restore

PY_PRINT_IO=$PFE_SCRIPT_DIR/postproc/print_io.py

it=$FIRST_PRINT_IO
while [ $it -le $LAST_PRINT_IO ]
do
    $PY_PRINT_IO $IO_HEAD_FILE $IO_DATA_FILE $it > $PFE_LOG_DIR/io_content.$it
    let "it+=1"
done
