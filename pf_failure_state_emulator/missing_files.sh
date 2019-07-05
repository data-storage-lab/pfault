#!/bin/sh

#input mgt_n_name or mdt_n_name or ost_n_name
#ssh mgs/mds/oss_n_user@mgs/mds/oss_n_ip 
#cd mgt/mdt/ost_n_ldiskfs_mountpoint
#percentage
  
<< EOF
    cd $1
NUMBER=$(ls -l | grep -v ^l | wc -l)
#echo $NUMBER
TOTAL=$(($RANDOM % $NUMBER + 1)) 
#echo $TOTAL
INPUT="ls |sort -R |tail -$TOTAL"
OUTPUT=$(eval $INPUT)
for i in "${OUTPUT[@]}"
do
	#if [ "$i" -ne "random.sh" ];
	#then 
	RMF="sudo rm -rf $i"	
	eval $RMF
	#fi
#	echo $i
done

EOF

it=0
while [ $it -lt $FAILURE_TARGET_CNT ]
do
    ssh ${FAILURE_TARGET_USERS[it]}@${FAILURE_TARGET_IPS[it]} << EOF
        cd ${FAILURE_TARGET_MNT_PNT[it]}
        num_files=`find $(pwd) -type f | wc -l`
        del_num_files=`echo $(( $num_files * $FAILURE_TARGET_DELETE_PCTG / 100  ))`
        
        for fl in `find $(pwd) -type f | shuf -n $del_num_files`;
        do
            #sudo rm -f $fl
            echo "Deleting: $fl"
        done

EOF

let "it+=1"

done

