#!/usr/bin/env bash

absme=`readlink -f $0`
abshere=`dirname $absme`
. $abshere/variables.sh
source configuration.sh
it=0
tid=1
##### Setup MGT Targets
while [ $it -lt $MGT_CNT ]
do
    
	#echo "Setup iSCSI target $tid"
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid $tid -T ${MGT_NAME[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid $tid --lun 1 -b $ISCSI_DIR/pfe_scripts/multinodes/img/${MGT_NAME[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op bind --mode target --tid $tid --initiator-address=${MGS_IP[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
	let "it+=1"
	let "tid+=1"

done 
##### Setup MDT Targets
it=0
while [ $it -lt $MDT_CNT ]
do
    
	#echo "Setup iSCSI target $tid"
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid $tid -T ${MDT_NAME[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid $tid --lun 1 -b $ISCSI_DIR/pfe_scripts/multinodes/img/${MDT_NAME[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op bind --mode target --tid $tid --initiator-address=${MDS_IP[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
	let "it+=1"
	let "tid+=1"

done
##### Setup OST Targets
it=0
while [ $it -lt $OST_CNT ]
do
    
	#echo "Setup iSCSI target $tid"
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid $tid -T ${OST_NAME[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid $tid --lun 1 -b $ISCSI_DIR/pfe_scripts/multinodes/img/${OST_NAME[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op bind --mode target --tid $tid --initiator-address=${OSS_IP[$it]}
	sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
	let "it+=1"
	let "tid+=1"

done

#echo "###### check tgtd started"
#check_tgtd


#echo "###### Setup iSCSI target 1 (tid = 1)"
#date
#echo "### define a target name and create a target "
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 1 -T $ISCSI_TARGET_NAME_1"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 1 -T $ISCSI_TARGET_NAME_1
#sudo ../usr/tgtadm  --lld iscsi --op new --mode target --tid 1 -T iqn.2013-01.diskfault:emulator

#echo "### add backing store"
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b $TGT_BS_1" 
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b $TGT_BS_1 
#sudo ../usr/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b /home/zhengm/iscsi-bs-512M

#echo "### enable the target to accept any initiator"
#sudo $PFE_USR_DIR/tgtadm   --lld iscsi --op bind --mode target --tid 1   --initiator-address=192.168.56.111 #-I ALL

#echo "### view the target created"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
#echo ""
#echo "###### TARGET 1 SETUP DONE!"


#echo ""
#echo "###### Setup iSCSI target 2 (tid = 2)"
#date
#echo "### define a target name and create a target "
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 2 -T $ISCSI_TARGET_NAME_2"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 2 -T $ISCSI_TARGET_NAME_2

#echo "### add backing store"
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 2 --lun 1 -b $TGT_BS_2" 
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 2 --lun 1 -b $TGT_BS_2 

#echo "### enable the target to accept any initiator"
#sudo $PFE_USR_DIR/tgtadm   --lld iscsi --op bind --mode target --tid 2  --initiator-address=192.168.56.110 #-I ALL

#echo "### view the target created"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
#echo ""
#echo "####### TARGET 2 SETUP DONE!"

#echo ""
#echo "###### Setup iSCSI target 3 (tid = 3)"
#date
##echo "### define a target name and create a target "
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 3 -T $ISCSI_TARGET_NAME_3"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 3 -T $ISCSI_TARGET_NAME_3

#echo "### add backing store"
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 3 --lun 1 -b $TGT_BS_3"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 3 --lun 1 -b $TGT_BS_3

#echo "### enable the target to accept any initiator"
#sudo $PFE_USR_DIR/tgtadm   --lld iscsi --op bind --mode target --tid 3 --initiator-address=192.168.56.129 #-I ALL


#echo "### view the target created"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target

#echo ""
#echo "###### Setup iSCSI target 4 (tid = 4)"
#date
#echo "### define a target name and create a target "
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 4 -T $ISCSI_TARGET_NAME_4"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 4 -T $ISCSI_TARGET_NAME_4

#echo "### add backing store"
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 4 --lun 1 -b $TGT_BS_4"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 4 --lun 1 -b $TGT_BS_4

#echo "### enable the target to accept any initiator"
#sudo $PFE_USR_DIR/tgtadm   --lld iscsi --op bind --mode target --tid 4 --initiator-address=192.168.56.108 #-I ALL


#echo "### view the target created"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
#echo ""


#echo ""
#echo "###### Setup iSCSI target 5 (tid = 5)"
#date
#echo "### define a target name and create a target "
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 5 -T $ISCSI_TARGET_NAME_5"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 5 -T $ISCSI_TARGET_NAME_5

#echo "### add backing store"
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 5 --lun 1 -b $TGT_BS_5"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 5 --lun 1 -b $TGT_BS_5

#echo "### enable the target to accept any initiator"
#sudo $PFE_USR_DIR/tgtadm   --lld iscsi --op bind --mode target --tid 5   --initiator-address=192.168.56.109 #-I ALL


#echo "### view the target created"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
#echo ""


#echo ""
#echo "###### Setup iSCSI target 6 (tid = 6)"
#date
#echo "### define a target name and create a target "
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 6 -T $ISCSI_TARGET_NAME_6"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 6 -T $ISCSI_TARGET_NAME_6

#echo "### add backing store"
#echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 6 --lun 1 -b $TGT_BS_6"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 6 --lun 1 -b $TGT_BS_6

#echo "### enable the target to accept any initiator"
#sudo $PFE_USR_DIR/tgtadm   --lld iscsi --op bind --mode target --tid 6  --initiator-address=192.168.56.112 #-I ALL


#echo "### view the target created"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
#echo ""


#echo "check port 3260"
#sudo netstat -tulpn | grep 3260
#echo ""


