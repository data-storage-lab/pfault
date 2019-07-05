#!/usr/bin/env bash
#setup iscsi initiator on debian
#Note:
#only need to discover and login for the very first time
#later(after re-run tgtd) just restart

#. ./pfe_global.sh
. $PFE_SCRIPT_DIR/pfe_helper.sh

echo "######### Setup iSCSI Initiator on Debian"
#echo "### rm old open-iscsi data"
#$PFE_SCRIPT_DIR/cleanup-openiscsi-deb.sh

echo "### restart iscsi"
sudo  /etc/init.d/open-iscsi restart

#echo "### discover target 164.107.119.55" 
#164.107.116.48 dachuan's 
#127.0.0.1 for local
#sudo iscsiadm --mode discovery --type sendtargets --portal 164.107.119.55

sudo iscsiadm --mode discovery --type sendtargets --portal $ISCSI_TARGET_IP 
#should output: 164.107.119.55:3260,1 iqn.2013-01.diskfault:emulator

#echo "### login"
#sudo iscsiadm --mode node --targetname iqn.2013-01.diskfault:emulator --portal 164.107.119.55:3260 --login
#sudo iscsiadm --mode node --targetname iqn.2013-01.diskfault:emulator --portal 127.0.0.1:3260 --login
sudo iscsiadm --mode node --targetname $ISCSI_TARGET_NAME --portal $ISCSI_TARGET_IP:3260 --login

echo "###### Initiator setup DONE!"


