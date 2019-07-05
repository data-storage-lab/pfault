#!/bin/sh

#input mgt_n_name or mdt_n_name or ost_n_name
#ssh mgs/mds/oss_n_user@mgs/mds/oss_n_ip 
#cd mgt/mdt/ost_n_ldiskfs_mountpoint
#percentage
#<< EOF

#random select a percentage of local files by injecting random bit

#EOF
it=0
while [ $it -lt $FAILURE_TARGET_CNT ]
do
    ssh ${FAILURE_TARGET_USERS[it]}@${FAILURE_TARGET_IPS[it]} << EOF
        cd ${FAILURE_TARGET_MNT_PNT[it]}
        num_files=`find $(pwd) -type f | wc -l`
        del_num_files=`echo $(( $num_files * $FAILURE_TARGET_CORRUPT_PCTG / 100  ))`
        
        for fl in `find $(pwd) -type f | shuf -n $del_num_files`;
        do
            #sudo rm -f $fl
            #echo "Deleting: $fl"
            fl_sz=`stat --printf="%s" $fl`
            seek_val=`shuf -i 1-$fl_sz -n 1`
            bt_range=$(( $fl_sz - $seek_val ))
            bt_count=`shuf -i 1-$bt_range -n 1`
            if [ $bt_count -gt $FAILURE_TARGET_CORRUPT_MAX_BITS ]
            then
                bt_count=$FAILURE_TARGET_CORRUPT_MAX_BITS
            fi
            sudo dd if=/dev/random of=$fl bs=1 count=$bt_count seek=$seek_val
        done

EOF

let "it+=1"

done
