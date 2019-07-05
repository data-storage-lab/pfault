#!/usr/bin/env bash

#set -x verbose

#. ./pfe_global.sh
. $PFE_SCRIPT_DIR/pfe_helper.sh

#IO range replayed in stage 3
REPLAY_END_IO=10000000000 #should be large enough to include all IO  

echo -e "################ STAGE #3 : REPLAY and CHECK\n"
date
#prepare base image
echo "######### cp baseimge for replay"
cp ${TGT_REPLAY_IMG_BASE} ${TGT_REPLAY_IMG_FAIL}
sleep 3

echo -e "\n######### REPLAY"
$REPLAYER --disk-file ${TGT_REPLAY_IMG_FAIL} --io-header-log ${WORKLOAD_IO_HEAD_LOG}\
    --io-header-split-log ${IO_HEAD_SPLIT_LOG}  --io-data-log ${WORKLOAD_IO_DATA_LOG}\
    --fail-type 0 --start-io  1 --end-io ${REPLAY_END_IO}\
    --pfe-err-blk ${ERR_BLOCK_LOG}  --split-io 1\
     2>&1 | tee $PFE_LOG_DIR/log.replay.0

if [[ $ENABLE_OD_IO == "true" ]]; then
	echo "od $WORKLOAD_IO_HEAD_LOG to $WORKLOAD_IO_HEAD_LOG.od"
	$PFE_SCRIPT_DIR/test-od.sh $WORKLOAD_IO_HEAD_LOG > $WORKLOAD_IO_HEAD_LOG.od 2>&1
	echo "od $WORKLOAD_IO_DATA_LOG to $WORKLOAD_IO_DATA_LOG.od"
	$PFE_SCRIPT_DIR/test-od.sh $WORKLOAD_IO_DATA_LOG > $WORKLOAD_IO_DATA_LOG.od 2>&1
	echo "od $IO_HEAD_SPLIT_LOG to $IO_HEAD_SPLIT_LOG.od"
	$PFE_SCRIPT_DIR/test-od.sh $IO_HEAD_SPLIT_LOG > $IO_HEAD_SPLIT_LOG.od 2>&1

    #if [ -e $STRACE_FILE ]; then
    	$PFE_SCRIPT_DIR/postproc/map_io2syscall.sh
    #fi
fi

sync;sync;sync

#save a copy of the splitted IO head log
echo "### save a copy of splitted IO head log"
cp $IO_HEAD_SPLIT_LOG $IO_HEAD_SPLIT_LOG.work 
sudo cp $IO_HEAD_SPLIT_LOG $IO_HEAD_SPLIT_RAMLOG #a copy in ram 
sudo chmod 777 $IO_HEAD_SPLIT_RAMLOG
sudo cp $IO_HEAD_SPLIT_LOG $IO_HEAD_SPLIT_RAMLOG.work #a copy in ram 
sudo chmod 777 $IO_HEAD_SPLIT_RAMLOG.work
echo -e "######### REPLAY DONE\n"
sleep 5





echo "sudo mount -t $PFE_FS -o loop $TGT_REPLAY_IMG_FAIL $MNT "
sudo mount -t $PFE_FS -o loop $TGT_REPLAY_IMG_FAIL $MNT 
#check_mount
echo "ls $MNT"
sudo ls -lsit $MNT
echo "ls -lsit $DB_ENVIRONMENT"
sudo ls -lsit  $DB_ENVIRONMENT

sync;sync

#################################### APP Check
echo -e "\n######### APP CHECK START"
date

LOG_FILE=$PFE_LOG_DIR/log.replay.0
TOT_IO_CNT=$(grep replayed $LOG_FILE | awk '{print $7}')
export CUT_IO_NUM=$TOT_IO_CNT
echo "CUT_IO_NUM = $CUT_IO_NUM"

echo $APP_CHECK
$APP_CHECK 2>&1 | tee $PFE_LOG_DIR/log.app-check
echo -e "######### APP CHECK DONE\n"
####################################


sleep 3
echo "ls $MNT"
sudo ls -lsit $MNT
echo "ls $DB_ENVIRONMENT"
sudo ls -lsit $DB_ENVIRONMENT

cd $PFE_SCRIPT_DIR 
#echo "### [initiator] umount $INIT_DEV"
sync;sync
echo "### sudo umount $MNT"
sudo umount $MNT
sleep 3
echo "ls $MNT"
ls -lsit $MNT



sudo rm -rf $MNT/*

echo -e "\n################ STAGE #3 DONE!"
date
