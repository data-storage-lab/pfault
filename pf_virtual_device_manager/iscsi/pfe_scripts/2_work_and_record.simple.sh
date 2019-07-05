#!/usr/bin/env bash
#do work and record IO seq.

#set -x verbose

#rm previous runs logs
sudo rm -rf $IO_HEAD_LOG
sudo rm -rf $IO_DATA_LOG
sudo rm -rf $IO_HEAD_SPLIT_LOG
sudo rm -rf $ERR_BLOCK_LOG
sudo rm -rf $IO_HEAD_SPLIT_RAMLOG

. $PFE_SCRIPT_DIR/pfe_helper.sh

echo -e "################ STAGE #2 : DO WORK and RECORD\n"
date
#prepare base image
echo "### cp baseimge for work"
cp ${TGT_REPLAY_IMG_BASE} ${TGT_WORK_IMG}
sleep 3

echo "### Setup iscsi target & initiator"
echo "run tgtd in background"
sudo $PFE_USR_DIR/tgtd --pfe-io-header-log ${IO_HEAD_LOG} --pfe-fail-type-tgtd 0 \
    --pfe-err-blk ${ERR_BLOCK_LOG} --pfe-io-data-log ${IO_DATA_LOG} --pfe-enable-record 1
#    --pfe-err-blk ${ERR_BLOCK_LOG} --pfe-io-data-log ${IO_DATA_LOG} --pfe-enable-record 1\
#    2>&1 | tee $PFE_LOG_DIR/log.tgtd.work

#setup target
$TARGET_SETUP_SH ${TGT_WORK_IMG}
sleep 3




#setup initiator
#$PFE_SCRIPT_DIR/initiator-restart-deb.sh 
$INITIATOR_SETUP_SH
sleep 3
#find iscsi dev file
timed_dev_probe
sleep 5

#mount/umount original backing image
echo "### [initiator] mount -t $PFE_FS -o noatime $INIT_DEV $MNT"
#sudo mount -t $PFE_FS -o loop $INIT_DEV $MNT 
sudo mount -t $PFE_FS -o noatime $INIT_DEV $MNT  
#make sure can mount
sleep 3
#check_mount
echo "ls $MNT"
sudo ls -lsit $MNT
echo "ls $DB_ENVIRONMENT"
sudo ls -lsit $DB_ENVIRONMENT

sync;sync

###################### WORKER DO WORK (tgtd record) 
echo -e "\n######### APP WORK (tgtd RECORD)"
echo $APP_WORK
$APP_WORK 2>&1 | tee $PFE_LOG_DIR/log.app-work
echo -e "######### APP WORK DONE\n"
######################

sleep 3
echo "ls $MNT"
sudo ls -lsit $MNT
echo "ls $DB_ENVIRONMENT"
sudo ls -lsit $DB_ENVIRONMENT

cd $PFE_SCRIPT_DIR 
echo "### [initiator] umount $INIT_DEV"
sync;sync
sudo umount $MNT
sleep 5 
echo "ls $MNT"
ls -lsit $MNT






echo "### [target] save work io logs"
#save a copy of the workloads' IO logs for replay
cp $IO_HEAD_LOG $WORKLOAD_IO_HEAD_LOG
cp $IO_DATA_LOG $WORKLOAD_IO_DATA_LOG

#save a copy of the tgtd log (if run tgtd in forground) 
if [ -f $TGTD_LOG ];then
    cp $TGTD_LOG $TGTD_LOG.work
fi

#on the same machine, so simply kill tgtd to end this IO sequence 
$PFE_SCRIPT_DIR/target-kill.sh
sleep 3
sudo rm -rf $MNT/*
echo -e "\n################ STAGE #2 DONE!"
date
