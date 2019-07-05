#!/usr/bin/env bash
#repeately replay with emulated failures & check

#set -x verbose

. $PFE_SCRIPT_DIR/pfe_helper.sh

echo -e "################ STAGE #4 : REPLAY AND CHECK REPEATEDLY\n"
date

######################################################## Config
#total IOs recorded; get from stage3 log.replay.0
LOG_FILE=$PFE_LOG_DIR/log.replay.0
TOT_IO_CNT=$(grep replayed $LOG_FILE | awk '{print $7}')
echo "TOT_IO_CNT = $TOT_IO_CNT"

#replay from last
CUT_START_IO=${TOT_IO_CNT} #start from last io
#or manually specifiy a cut io 
#CUT_START_IO=1392

#let "CUT_STOP_IO = $CUT_START_IO - 2" #replay last 2+1 IOs
#CUT_STOP_IO=1 #replay all IOs

#fsck 
ENABLE_FSCK=true

#debugfs
#ENABLE_DEBUGFS=true
ENABLE_DEBUGFS=false
##########################################################

#base image in ram 
sudo cp ${TGT_REPLAY_IMG_BASE} ${TGT_REPLAY_RAMIMG_BASE}
sudo chmod 777  ${TGT_REPLAY_RAMIMG_BASE}

#signature of this run
THISDATE=`date +"%m%d"`
THISTIME=`date +"%T" | sed s/":"//g`
THIS=$THISDATE$THISTIME


one_cut() {
    echo -e "\n============================================ Cut at IO# ${it}"
    date

    #prepare base image
    echo "######### cp ram baseimge for replay in ram"
    sudo cp ${TGT_REPLAY_RAMIMG_BASE} ${TGT_REPLAY_RAMIMG_FAIL}
	sudo chmod 777 ${TGT_REPLAY_RAMIMG_FAIL}

    ############################### REPLAY
    echo "######### REPLAY"
    if [ ! -f $IO_HEAD_SPLIT_RAMLOG.work ];then
        #haven't spitted IO; use io logs on disk
        echo "No $IO_HEAD_SPLIT_RAMLOG.work, split IO and replay ..."
        $REPLAYER --disk-file ${TGT_REPLAY_RAMIMG_FAIL} --io-header-log ${WORKLOAD_IO_HEAD_LOG}\
            --io-header-split-log ${IO_HEAD_SPLIT_RAMLOG}  --io-data-log ${WORKLOAD_IO_DATA_LOG}\
            --fail-type ${THIS_FAIL_TYPE} --start-io 1  --end-io ${it}\
            --pfe-err-blk ${ERR_BLOCK_LOG}  --split-io 1 #\
            # 2>&1 | tee $PFE_LOG_DIR/log.replay.$THIS.$it
            # 2>&1 | tee $PFE_LOG_DIR/log.replay.$it
        #save a copy of the splitted IO head log
        sudo cp $IO_HEAD_SPLIT_RAMLOG $IO_HEAD_SPLIT_RAMLOG.work 
    else
        #already spltted IO in previous runs; use ram io header log
        echo "Found $IO_HEAD_SPLIT_RAMLOG.work, replaying ..."
        $REPLAYER --disk-file ${TGT_REPLAY_RAMIMG_FAIL} --io-header-log ${IO_HEAD_SPLIT_RAMLOG}.work\
            --io-header-split-log ${IO_HEAD_SPLIT_RAMLOG}.work  --io-data-log ${WORKLOAD_IO_DATA_LOG}\
            --fail-type ${THIS_FAIL_TYPE} --start-io 1  --end-io ${it}\
            --pfe-err-blk ${ERR_BLOCK_LOG}  --split-io 0 #\
            # 2>&1 | tee $PFE_LOG_DIR/log.replay.$it
    fi
    echo "######### REPLAY DONE"
    ##############################
    #sync;sync

    #echo "######### Setup iSCSI target & initiator"
    ##run tgtd in background 
    #echo "run tgtd in background"
    #sudo $PFE_USR_DIR/tgtd --pfe-io-header-log ${IO_HEAD_LOG} --pfe-fail-type-tgtd ${THIS_FAIL_TYPE} \
    #    --pfe-err-blk ${ERR_BLOCK_LOG} --pfe-io-data-log ${IO_DATA_LOG} --pfe-enable-record 0 
    #sleep 1
    #setup target
    #$TARGET_SETUP_SH $TGT_REPLAY_RAMIMG_FAIL
    #sleep 1
    #setup initiator 
    #$INITIATOR_SETUP_SH
    #sleep 1
    #find iscsi dev file
    #timed_dev_probe
    #sleep 1
    #echo "######## Setup iSCSI DONE"

    

    #if [[ "$ENABLE_FSCK" == "true" ]]; then
    #    echo "######## fsck $INIT_DEV"
    #    sudo fsck -t $PFE_FS -a $INIT_DEV 
    #fi 
    if [[ "$ENABLE_FSCK" == "true" ]]; then
        echo "######## fsck $TGT_REPLAY_RAMIMG_FAIL"
        sudo fsck -t $PFE_FS -a $TGT_REPLAY_RAMIMG_FAIL
    fi 

	#echo "######### [initiator] mount -t $PFE_FS  $INIT_DEV to $MNT"
    #umount first to make sure it's clean
    echo "######## sudo umount $MNT"
    sudo umount $MNT
    echo "ls -lsit $MNT"
    ls -lsit $MNT

    #sudo mount -t $PFE_FS $INIT_DEV $MNT 
    echo "sudo mount -t $PFE_FS -o loop $TGT_REPLAY_RAMIMG_FAIL $MNT"
    sudo mount -t $PFE_FS -o loop $TGT_REPLAY_RAMIMG_FAIL $MNT 
    echo "ls -lsit $MNT"
    sudo ls -lsit $MNT
    echo "ls -lsit $DB_ENVIRONMENT"
    sudo ls -lsit  $DB_ENVIRONMENT

    #################################### APP Check
    echo -e "\n######### APP CHECK START"
    date

    export CUT_IO_NUM=$it

    $APP_CHECK

    echo -e "######### APP CHECK DONE"
    echo -e "CUT_IO_NUM = $CUT_IO_NUM \n"
    date
    ####################################

    echo "ls $MNT"
    sudo ls -lsit $MNT
    echo "ls $DB_ENVIRONMENT"
    sudo ls -lsit $DB_ENVIRONMENT
    cd $PFE_SCRIPT_DIR 
    sync;sync
    sleep 1


    #echo "######### [initiator] umount -f $INIT_DEV"
    #echo "######## kill oracle"
    #. $PFE_SCRIPT_DIR/kill-oracle.sh
    echo "######## sudo umount $MNT"
    sudo umount $MNT
    echo "ls -lsit $MNT"
    ls -lsit $MNT

    #echo "######### [target] save logs"
    #save a copy of the IO logs
    #cp $IO_HEAD_LOG $IO_HEAD_LOG.check.$THIS.$it
    #cp $IO_DATA_LOG $IO_DATA_LOG.check.$THIS.$it
    #save a copy of the tgtd log 
    #cp $TGTD_LOG $TGTD_LOG.check.$THIS.$it

    #echo "######### [target] kill tgtd"
    #on the same machine, so simply kill tgtd to end this IO sequence 
    #$PFE_SCRIPT_DIR/target-kill.sh
    #echo "######### [target] cleanup"
    #$PFE_SCRIPT_DIR/cleanup.sh

    echo "######### #${it} DONE"
	
    if [[ "$ENABLE_DEBUGFS" == "true" ]]; then
		echo $DEBUGFS_DIR
		SAVED_IMG=$DEBUGFS_DIR/replayed_img.cut-$it 
		echo "####### save $TGT_REPLAY_RAMIMG_FAIL to $SAVED_IMG for debugfs"
    	sudo cp ${TGT_REPLAY_RAMIMG_FAIL} $SAVED_IMG
		echo "###fsck $SAVED_IMG"
        sudo fsck -t $PFE_FS  -p $SAVED_IMG 
	fi
}


############## Cut method 1: cut at every io
if [[ $CUT_OPTION == "EXHAUSTIVE_CUT" ]]; then
    cut_cnt=0

    CUT_START_IO=${TOT_IO_CNT} #start from last io
    #let "CUT_STOP_IO = $CUT_START_IO - 1" #replay last 1+1 IOs
    CUT_STOP_IO=1 #replay all IOs

    echo "CUT_OPTION == $CUT_OPTION "
    echo "CUT_START_IO == $CUT_START_IO"
    echo "CUT_STOP_IO == $CUT_STOP_IO"

    it=$CUT_START_IO
    while [ ${it} -ge ${CUT_STOP_IO} ] #cut from last IO
    do
        one_cut
        let "it-=1" #cut from last IO
        let "cut_cnt += 1"
    done 
fi

############## Cut method 2: sampling
if [[ $CUT_OPTION == "SAMPLING_CUT" ]]; then
    cut_cnt=0

    RAND_SEQ_LENGTH=$TOT_IO_CNT
    SAMPLE_CNT=$(( RAND_SEQ_LENGTH * SAMPLE_PERCENTAGE / 100 ))

    echo -e "\nCUT_OPTION = $CUT_OPTION"
    echo "SAMPLE_PERCENTAGE = $SAMPLE_PERCENTAGE"
    echo "TOT_IO_CNT = $TOT_IO_CNT"

    sample_io
    for it in $(cat $SAMPLE_FILE); do
        echo "$it"
        one_cut
        let "cut_cnt += 1"
    done

fi


############## Cut method 3: pattern

if [[ $CUT_OPTION == "PATTERN_CUT" ]]; then
    cut_cnt=0

    #RAND_SEQ_LENGTH=$TOT_IO_CNT
    #SAMPLE_CNT=$(( RAND_SEQ_LENGTH * SAMPLE_PERCENTAGE / 100 ))

    echo -e "\nCUT_OPTION = $CUT_OPTION"
    echo "CUT_PATTERN_FILE = $CUT_PATTERN_FILE"
    echo "TOT_IO_CNT = $TOT_IO_CNT"

    for it in $(cat $CUT_PATTERN_FILE); do
        echo "$it"
        one_cut
        let "cut_cnt += 1"
    done

fi



echo -e "\n========================================================="
date
echo "Testing Completed Successfully!"
echo "Total # of IO = $TOT_IO_CNT"
echo "CUT_OPTION = $CUT_OPTION"
echo "Total # of cuts in this run = $cut_cnt"
echo -e "=================== STAGE #4 ALL DONE ===================\n"
exit 0
