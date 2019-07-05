#!/usr/bin/env bash
#testing mulitple targets

absme=`readlink -f $0`
abshere=`dirname $absme`
. $abshere/variables.sh

echo "###### check tgtd started"
check_tgtd


echo "###### Setup iSCSI target 1 (tid = 1)"
date
echo "### define a target name and create a target "
echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 1 -T $ISCSI_TARGET_NAME_1"
sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 1 -T $ISCSI_TARGET_NAME_1
#sudo ../usr/tgtadm  --lld iscsi --op new --mode target --tid 1 -T iqn.2013-01.diskfault:emulator

echo "### add backing store"
echo "sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b $TGT_BS_1" 
sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b $TGT_BS_1 
#sudo ../usr/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b /home/zhengm/iscsi-bs-512M

echo "### enable the target to accept any initiator"
sudo $PFE_USR_DIR/tgtadm   --lld iscsi --op bind --mode target --tid 1 -I ALL

echo "### view the target created"
sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
echo ""
echo "###### TARGET 1 SETUP DONE!"


echo "check port 3260"
sudo netstat -tulpn | grep 3260
echo ""


