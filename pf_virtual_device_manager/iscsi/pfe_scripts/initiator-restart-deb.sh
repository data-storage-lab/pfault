#!/usr/bin/env bash

echo "######### Setup iSCSI Initiator on Debian"
#echo "### rm old open-iscsi data"
#$PFE_SCRIPT_DIR/cleanup-openiscsi-deb.sh
echo "###### Initiator restart iscsi"
sudo  /etc/init.d/open-iscsi restart
#don't need to discover target and login

echo "###### INITIATOR SETUP DONE!"


