#!/usr/bin/env bash
#
##e.g.: ./THISFILE  /SOME/PATH/logs-tc-

absme=`readlink -f $0`
abshere=`dirname $absme`

#LOGS_MAIN_DIR=$1

for dir in $1*; do
    echo -e "\n#=================== $dir ...\n"
    PFE_LOG_DIR=$dir
    $abshere/checker_driver_singlelog.sh $PFE_LOG_DIR
done
