#!/bin/bash

#print db's *.err files in a range of cuts
#./THISFILE LOG_PATH SMALLEST_IO LARGEST_IO ERR_FILE_NAME
#./maria_errmsg.sh /home/zhengm/logs-folder/logs-maria-wkld4_THR-1-TXN-10-KEY-10_fail-0-unseri-small-fs-xfs-cutopt-EXHAUSTIVE_CUT-100.140227135849.replay.667-675 667 675 fengqin-pc.err

LOG_DIR=$1
SMALLEST_IO=$2
LARGEST_IO=$3
ERR_FILE_NAME=$4
#ERR_FILE_NAME=fengqin-pc.err #maria err file

get_err_msg(){
    tmp_mnt=./mnt
    mkdir $tmp_mnt
    sudo mount $LOG_DIR/$img $tmp_mnt -o loop
    cat $tmp_mnt/$ERR_FILE_NAME > $LOG_DIR/$img.err
    sleep 3
    sudo umount $tmp_mnt
    sleep 1
    rmdir $tmp_mnt
}

it=$LARGEST_IO
while [ ${it} -ge ${SMALLEST_IO} ] #
do
	img=img.$it.2fscked
    get_err_msg
	img=img.$it.3checked
    get_err_msg

    let "it-=1" #
done


#diff
absme=`readlink -f $0`
abshere=`dirname $absme`
$abshere/diff_err23.sh $LOG_DIR $SMALLEST_IO $LARGEST_IO


