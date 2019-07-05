#!/usr/bin/env bash
#. ./pfe_global.sh
. $PFE_SCRIPT_DIR/pfe_helper.sh

if (( $# > 0 )); then
    BS_FILE=$1
fi

date
echo "###### Setup iSCSI target"

#echo "### start tgtd process"
# "-f, --foreground        make the program run in the foreground\n"
# "-d, --debug debuglevel  print debugging information\n"
#sudo ../usr/tgtd  

echo "### check tgtd started"
#sudo ps -df|grep -i tgt
check_tgtd

date
echo "### define an iscsi target name"
#sudo ../usr/tgtadm  --lld iscsi --op new --mode target --tid 1 -T iqn.2013-01.diskfault:emulator
sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode target --tid 1 -T $ISCSI_TARGET_NAME
#echo "### view the target created"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
#echo ""

echo "### add a $BS_FILE as backing store"
#create imgae if necessary
if [ ! -f $BS_FILE ];then
    echo "no $BS_FILE, creating one ..."
    dd if=/dev/zero of=$BS_FILE bs=$DD_BS count=$DD_COUNT oflag=sync
fi

sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b $BS_FILE 
#sudo ../usr/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b /home/zhengm/iscsi-bs-512M
#sudo ./usr/tgtadm  --lld iscsi --op new --mode logicalunit --tid 1 --lun 1 -b /dev/sdb
#echo "### view the target created"
#sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target  
#echo ""

echo "### enable the target to accept any initiator"
sudo $PFE_USR_DIR/tgtadm   --lld iscsi --op bind --mode target --tid 1 -I ALL
echo "### view the target created"
sudo $PFE_USR_DIR/tgtadm  --lld iscsi --op show --mode target
echo ""

echo "check port 3260"
sudo netstat -tulpn | grep 3260
echo ""

echo "####### TARGET SETUP DONE!"

### on the same machine, so we can setup initiator here
#./initiator-restart-deb.sh
