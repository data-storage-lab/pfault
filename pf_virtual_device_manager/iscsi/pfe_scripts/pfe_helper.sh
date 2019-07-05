#!/usr/bin/env bash

############ prepare necessary files 
#create imgae if necessary
if [ ! -f $TGT_IMG ];then
    echo "no $TGT_IMG, creating one ..."
    sudo dd if=/dev/zero of=$TGT_IMG bs=$DD_BS count=$DD_COUNT oflag=sync
    sudo chmod 666 $TGT_IMG
fi

#avoid no file / wrong permission
if [ ! -d $PFE_LOG_DIR ];then
    echo "no $PFE_LOG_DIR, creating one ..."
    sudo mkdir $PFE_LOG_DIR
    sudo chmod 755 $PFE_LOG_DIR
fi
sudo chmod -R 777 $APP_DIR
sudo touch $IO_HEAD_LOG
sudo touch $IO_DATA_LOG
sudo touch $IO_HEAD_SPLIT_LOG
sudo touch $ERR_BLOCK_LOG
sudo touch $IO_HEAD_SPLIT_RAMLOG
sudo chmod 666 $IO_HEAD_LOG
sudo chmod 666 $IO_DATA_LOG
sudo chmod 666 $IO_HEAD_SPLIT_LOG
sudo chmod 666 $ERR_BLOCK_LOG
sudo chmod 666 $IO_HEAD_SPLIT_RAMLOG



############ helper functions

#probe iscsi device on initiator side
timed_dev_probe() {
    echo "PFE: probing VIRTUAL-DISK ..."
    SSD_MODEL="VIRTUAL-DISK    "
        TIME_LIMIT=60 #max probe time
        INIT_T=$(date +%s)
        PROBE_DISK_FILE=0;
        while [ $PROBE_DISK_FILE == 0 ]
        do
                for drive in b c d e f g h i j k l m n o p q r s t u v w x y z; do 
                        if [ -e "/dev/sd${drive}" ]; then
                                drive_size=`cat /sys/block/sd${drive}/size`
                                drive_model=`cat /sys/block/sd${drive}/device/model` # | sed s//-/g`
                                #if [[ "$drive_size" == "$SSD_SIZE"  &&  "$drive_model" == "$SSD_MODEL" ]]; then
                                if [[ "$drive_model" == "$SSD_MODEL" ]]; then
                                        PROBE_DISK_FILE="/dev/sd${drive}"
                                        echo "Found [${PROBE_DISK_FILE}]!"
                                        #echo "size matched: [$drive_size]"
                                        echo "model matched: [$drive_model]"
                                        echo "Safe to use this iscsi device! "
                                        ls -l /dev/sd${drive}
                                        echo "sudo  chmod o+rw /dev/sd${drive}"
                                        sudo chmod o+rw /dev/sd${drive}
                                        ls -l /dev/sd${drive}
                                        sleep 1
                                        echo ""
                                        export INIT_DEV=/dev/sd${drive}
                                        break;
                                fi
                        fi
                done
                NOW_T=$(date +%s)
                ELAPSED_T=$(($NOW_T-$INIT_T))
                if [ "$ELAPSED_T" -gt "$TIME_LIMIT" ]; then
                    echo "Failed to find iscsi device in $TIME_LIMIT seconds!"
				    
                    exit 0
					#if [ -e $PFE_AUTORESUME_ENABLED ]; then
					#	echo "Found $PFE_AUTORESUME_ENABLED, rebooting ..."
	                #    sudo reboot #have implemented on apollo
		            #	exit 0
					#fi
                fi
        done
}


#check iscsi device is mounted
check_mount(){ #seems problematic
    MNT_DIR=$MNT
    #if grep -qs '$MNT_DIR' /proc/mounts; then
    #    echo "$MNT_DIR is mounted."
    #else
    #    echo "$MNT_DIR is not mounted."
    #    $PFE_SCRIPT_DIR/target-kill.sh
    #    exit 0
    #fi
}

#check tgtd is running
check_tgtd(){
    P_NAME=tgtd
    PROCESS_NUM=$(pgrep -f "$P_NAME" | wc -l)
    if [ $PROCESS_NUM -eq "0" ];then
            echo "!!!PFE_ERROR: no tgtd!!!"
            exit 0
    else
            echo "tgtd exists."
    fi
}

abspath(){ 
    case "$1" in 
        /*)
            printf "%s\n" "$1"
            ;; 
        *)
            printf "%s\n" "$PWD/$1"
            ;; esac; 
}

############# sample io

init_files(){
    if [ -z "$SEQ_FILE" ];then
        echo "!!!PFE_ERROR: no SEQ_FILE env var"
        exit 0
    fi
    if [ -z "$SHUF_FILE" ];then
        echo "!!!PFE_ERROR: no SHUF_FILE env var"
        exit 0
    fi
    cat /dev/null > $SEQ_FILE
    cat /dev/null > $SHUF_FILE
}

get_seq(){
    if [ -z "$RAND_SEQ_LENGTH" ];then
        echo "!!!PFE_ERROR: no RAND_SEQ_LENGTH env var"
        exit 0
    fi

    it=1
    while [ $it -le $RAND_SEQ_LENGTH ]; do
        echo $it >> $SEQ_FILE
        let "it+=1"
    done
}


shuf_seq(){
    cat $SEQ_FILE | shuf > $SHUF_FILE
}

sample_io(){
    init_files
    get_seq
    shuf_seq
    if [ -z "$SAMPLE_CNT" ];then
        echo "!!!PFE_ERROR: no SAMPLE_CNT env var"
        exit 0
    fi
    head -n $SAMPLE_CNT $SHUF_FILE > $SAMPLE_FILE 
}
