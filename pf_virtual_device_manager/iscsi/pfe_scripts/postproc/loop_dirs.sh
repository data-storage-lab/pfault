#!/bin/bash
#loop through a set of directories w/ common prefix
#
#./THISFILE LOG_NAME_LIKE_logs-
#e.g.: ./THISFILE  /SOME/PATH/logs-tc-

for dir in $1*; do
    echo $dir
    cd $dir

    FILE_NAME=newck.*
    PATTERN=Err
    grep $PATTERN $FILE_NAME | tee tmp

    cd ..
done
