#!/usr/bin/env bash

date
echo "######### Show iSCSI Target"

echo "### check tgtd started"
sudo ps -df|grep -i tgt
echo ""

echo "check port 3260"
sudo netstat -tulpn | grep 3260
echo ""

echo "### view the target created"
sudo ../usr/tgtadm --lld iscsi --op show --mode target
echo ""

echo "######### DONE!"
