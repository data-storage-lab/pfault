#!/bin/bash

CURRENT_DIR=`pwd`
PARENT_DIR=`dirname $CURRENT_DIR`
CONFIG_DIR=$PARENT_DIR/configuration/configuration.sh
source $CONFIG_DIR
scp $CONFIG_DIR $ISCSI_SERVER_USER@$ISCSI_SERVER_IP:$ISCSI_DIR/pfe_scripts/multinodes/configuration.sh
ssh $ISCSI_SERVER_USER@$ISCSI_SERVER_IP <<EOF
	
	sudo chmod 777 $ISCSI_DIR/pfe_scripts/multinodes/configuration.sh
	$ISCSI_DIR/pfe_scripts/multinodes/bk_create.sh 
        sleep 2
	$ISCSI_DIR/pfe_scripts/multinodes/target-run-tgtd.sh 
        sleep 2
        $ISCSI_DIR/pfe_scripts/multinodes/target-setup.sh
        sleep 10

	EOF

it=0
while [ $it -lt $MGS_CNT ]
do
	
	ssh ${MGS_USER[it]}@${MGS_IP[it]} <<EOF
		iscsiadm --mode discovery --type sendtargets --portal $ISCSI_SERVER_IP:3260
		sleep 2
		iscsiadm --mode node --targetname ${MGT_NAME[it]} --portal $ISCSI_SERVER_IP:3260 --login
		sleep 2
		mkfs.lustre --fsname=$LUSTRE_NAME --mgsnode=${MGS_IP[0]}@${MGS_LNET_POSTFIX[0]} --mgs -- reformat ${MGT_DISK_LABEL[it]}        
		sleep 5
		mount.lustre ${MGT_DISK_LABEL[it]} ${MGT_LUSTRE_MNT_PNT[it]}
		sleep 2
		mount -t ldiskfs ${MGT_DISK_LABEL[it]} ${MGT_LDISKFS_MNT_PNT[it]}
		sleep 2
	EOF
	let "it+=1"

done

it=0
while [ $it -lt $MDS_CNT ]
do
	ssh ${MDS_USER[it]}@${MDS_IP[it]} <<EOF
		iscsiadm --mode discovery --type sendtargets --portal $ISCSI_SERVER_IP:3260
		sleep 2
		iscsiadm --mode node --targetname ${MDT_NAME[it]} --portal $ISCSI_SERVER_IP:3260 --login
		sleep 2
		mkfs.lustre --fsname=$LUSTRE_NAME --mgsnode=${MGS_IP[0]}@${MGS_LNET_POSTFIX[0]} --mdt --index=$it --reformat ${MDT_DISK_LABEL}
		sleep 5
		mount.lustre ${MDT_DISK_LABEL[it]} ${MDT_LUSTRE_MNT_PNT[it]}
		sleep 2
		mount -t ldiskfs ${MDT_DISK_LABEL[it]} ${MDT_LDISKFS_MNT_PNT[it]}
		sleep 2
	EOF
	let "it+=1"

done

it=0
while [ $it -lt $OST_CNT ]
do

	ssh ${OSS_USER[it]}@${OSS_IP[it]} <<EOF
		iscsiadm --mode discovery --type sendtargets --portal $ISCSI_SERVER_IP:3260
		sleep 2
		iscsiadm --mode node --targetname ${OST_NAME[it]} --portal $ISCSI_SERVER_IP:3260 --login
		sleep 2
		mkfs.lustre --fsname=$LUSTRE_NAME --mgsnode=${MGS_IP[0]}@${MGS_LNET_POSTFIX[0]} --ost --index=$it --reformat ${OST_DISK_LABEL[it]}
		sleep 5
		mount.lustre ${OST_DISK_LABEL[it]} ${OST_LUSTRE_MNT_PNT[it]}
		sleep 2
		mount -t ldiskfs ${OST_DISK_LABEL[it]} ${OST_LDISKFS_MNT_PNT[it]}
		sleep 2
	EOF
	let "it+=1"

done

it=0
while [ $it -lt $CLIENT_CNT ]
do

	ssh ${CLIENT_USER[it]}@${CLIENT_IP[it]} <<EOF
		mount.lustre ${MGS_IP[0]}@${MGS_LNET_POSTFIX[0]}:/$LUSTRE_NAME $CLIENT_LUSTRE_MNT_PNT[it]
		sleep 2
		lfs setstripe -i 0 -c -1 -S 64K $CLIENT_LUSTRE_MNT_PNT
		lfs df -h
	EOF
	let "it+=1"

done
