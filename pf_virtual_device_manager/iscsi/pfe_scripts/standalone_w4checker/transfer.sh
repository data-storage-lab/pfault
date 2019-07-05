#!/usr/bin/env bash

absme=`readlink -f $0`
abshere=`dirname $absme`

LOGS_MAIN_DIR=$1

for directory in $LOGS_MAIN_DIR/logs-*fail-4*; do
    
    newck_dir=$directory.newck
    mkdir $newck_dir
    mv  $directory/newck.output* $newck_dir 
    scp -r $newck_dir apollo:/home/zhengm/LOGS

done
