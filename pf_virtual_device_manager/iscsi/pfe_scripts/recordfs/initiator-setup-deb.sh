#!/usr/bin/env bash
#testing multiple initiators on one machine

absme=`readlink -f $0`
abshere=`dirname $absme`
. $abshere/variables.sh

echo "######### Setup iSCSI Initiators"

echo "### restart iscsi"
sudo  /etc/init.d/open-iscsi restart

echo "### discover target 1" 
#127.0.0.1 for local
#sudo iscsiadm --mode discovery --type sendtargets --portal 164.107.119.55
echo "sudo iscsiadm --mode discovery --type sendtargets --portal $ISCSI_TARGET_IP_1" 
sudo iscsiadm --mode discovery --type sendtargets --portal $ISCSI_TARGET_IP_1 

echo "### login target 1"
#sudo iscsiadm --mode node --targetname iqn.2013-01.diskfault:emulator --portal 164.107.119.55:3260 --login
echo "sudo iscsiadm --mode node --targetname $ISCSI_TARGET_NAME_1 --portal $ISCSI_TARGET_IP_1:3260 --login"
sudo iscsiadm --mode node --targetname $ISCSI_TARGET_NAME_1 --portal $ISCSI_TARGET_IP_1:3260 --login


echo "###### Initiators  setup DONE!"


