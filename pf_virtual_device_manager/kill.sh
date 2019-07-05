#!/bin/bash

CURRENT_DIR=`pwd`
PARENT_DIR="$(dirname "$CURRENT_DIR")"
CONFIG_DIR=$PARENT_DIR/configuration/configuration.sh
source $CONFIG_DIR
it=0
while [ $it -lt $CLIENT_CNT ]
do
 ssh ${CLIENT_USER[it]}@${CLIENT_IP[it]} <<EOF
  umount -t lustre ${CLIENT_LUSTRE_MNT_PNT[it]}
EOF
 let "it+=1"
done

it=0
while [ $it -lt $OST_CNT ]
do
 ssh ${OSS_USER[it]}@${OSS_IP[it]} <<EOF
  umount ${OST_DISK_LABEL[it]}
  sleep 2
  umount ${OST_DISK_LABEL[it]}
  sleep 2
EOF
 let "it+=1"
done

it=0
while [ $it -lt $MDS_CNT ]
do
 ssh ${MDS_USER[it]}@${MDS_IP[it]} <<EOF
  umount ${MDT_DISK_LABEL[it]}
  sleep 2
  umount ${MDT_DISK_LABEL[it]}
  sleep 2
EOF
 let "it+=1"
done

it=0
while [ $it -lt $MGS_CNT ]
do
 ssh ${MGS_USER[it]}@${MGS_IP[it]} <<EOF
  umount ${MGT_DISK_LABEL[it]}
  sleep 2
  umount ${MGT_DISK_LABEL[it]}
  sleep 2
EOF
 let "it+=1"
done

ssh ${ISCSI_SERVER_USER}@${ISCSI_SERVER_IP} <<EOF
 $ISCSI_DIR/pfe_scripts/multinodes/target-kill.sh
EOF
