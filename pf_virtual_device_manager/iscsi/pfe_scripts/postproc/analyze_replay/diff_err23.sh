#!/bin/bash

#diff err msgs of a range of (replayed) )IO
#./THISFILE LOG_PATH SMALLEST_IO LARGEST_IO
#./THISFILE /home/zhengm/logs-folder/logs-maria-wkld4_THR-1-TXN-10-KEY-10_fail-0-unseri-small-fs-xfs-cutopt-EXHAUSTIVE_CUT-100.140227135849.replay.667-675 667 675

LOG_DIR=$1
SMALLEST_IO=$2
LARGEST_IO=$3

it=$LARGEST_IO
while [ ${it} -ge ${SMALLEST_IO} ] #
do
    output=$LOG_DIR/err23diff.$it
    img1=$LOG_DIR/img.$it.2fscked.err
    img2=$LOG_DIR/img.$it.3checked.err 
    echo  "diff $img1 $img2" > $output
    diff $img1 $img2  >> $output

    let "it-=1" #
done


