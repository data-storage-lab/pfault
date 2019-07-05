#!/usr/bin/env bash

#PFE internal directories/files/configs


################## Scripts & executable
export APP_INIT=${APP_DIR}/app-init.sh
export APP_WORK=${APP_DIR}/app-work.sh
export APP_CHECK=${APP_DIR}/app-check.sh
#replay Program
export REPLAYER=$PFE_USR_DIR/pfe_replay
#pattern files
export UNSERIAL_PATTERN_FILE=$PFE_SCRIPT_DIR/patterns/pattern.unserial.$UNSERIAL_PATTERN.txt
#files for sampling
export SEQ_FILE=$PFE_LOG_DIR/tmp.io-seq
export SHUF_FILE=$PFE_LOG_DIR/tmp.io-shuf
export SAMPLE_FILE=$PFE_LOG_DIR/tmp.io-sample

export STRACE_FILE=$PFE_LOG_DIR/strace-worklog.txt

################ Disk Images
export IMG_SIZE_MB=128 #backing store file size in MB
export IMG_NAME=iscsi-bs-${IMG_SIZE_MB}M
#dd param for zeroing bs image
export DD_BS=1M
export DD_COUNT=${IMG_SIZE_MB}
#target side backing store image
export TGT_IMG=${PFE_LOG_DIR}/${IMG_NAME}
#image in ram
export RAMDISK=${RAMDISK:=/dev/shm}
export TGT_RAMIMG=${RAMDISK}/${IMG_NAME}
#target side image for do work
export TGT_WORK_IMG=${TGT_IMG}.work
#target side image for replay
export TGT_REPLAY_IMG=${TGT_IMG}.re
#target side base image (where replay starts from)
export TGT_REPLAY_IMG_BASE=${TGT_IMG}.base
#target side image for repaly w/ failure
export TGT_REPLAY_IMG_FAIL=${TGT_IMG}.fail
#images in ram
export TGT_REPLAY_RAMIMG_BASE=${TGT_RAMIMG}.base
export TGT_REPLAY_RAMIMG_FAIL=${TGT_RAMIMG}.fail


################## iSCSI 
export ISCSI_TARGET_NAME=iqn.2013-03.diskfault:pfe
export ISCSI_TARGET_IP=127.0.0.1 #local 

#initiator side iscsi device
#export INIT_DEV=/dev/sdb #fake; will detect dynamically
#default backing store for setup target device

export BS_FILE=$TGT_IMG
#script for setup target
export TARGET_SETUP_SH=$PFE_SCRIPT_DIR/target-setup.sh 
#script for setup initiator
export INITIATOR_SETUP_SH=$PFE_SCRIPT_DIR/$INITIATOR_SETUP_FILE #may need change


################ Logs
#run 1-4 log
export STAGE_1_LOGNAME=log-1
export STAGE_2_LOGNAME=log-2
export STAGE_3_LOGNAME=log-3
export STAGE_4_LOGNAME=log-4
#names of default IO logs
export IO_HEAD_LOG=$PFE_LOG_DIR/pfe_io_head_log
export IO_DATA_LOG=$PFE_LOG_DIR/pfe_io_data_log
export IO_HEAD_SPLIT_LOG=${PFE_LOG_DIR}/pfe_io_head_split_log
export ERR_BLOCK_LOG=${PFE_LOG_DIR}/pfe_err_block_log
export TGTD_LOG=${PFE_LOG_DIR}/log.tgtd
#names of workload IO logs for replay 
export WORKLOAD_IO_HEAD_LOG=$IO_HEAD_LOG.work
export WORKLOAD_IO_DATA_LOG=$IO_DATA_LOG.work
#logs in ram
export IO_HEAD_SPLIT_RAMLOG=${RAMDISK}/pfe_io_head_split_log
#enable od IO logs
export ENABLE_OD_IO=true


################ debugfs
export DEBUGFS_DIR=/tmp 

