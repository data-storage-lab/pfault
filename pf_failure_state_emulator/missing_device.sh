#!/bin/bash

#source $PFAULT_DIR/configuration_example.sh
#cp $PFAULT_DIR/pf_failure_state_emulator/failure_node_configuration_template.sh as $PFAULT_DIR/#pf_failure_state_emulator/failure_node_configuration.sh and fill it out 
CURRENT_DIR=`pwd`
PARENT_DIR=`dirname $CURRENT_DIR`
CONFIG_DIR=$PARENT_DIR/configuration/configuration.sh
echo $CONFIG_DIR
source $CONFIG_DIR
echo $CONFIG_DIR
source $PFAULT_DIR/pf_failure_state_emulator/failure_node_configuration.sh
echo $CONFIG_DIR

it=0
while [ $it -lt $FAILURE_TARGET_CNT ]
do
 ssh ${FAILURE_TARGET_USERS[it]}@${FAILURE_TARGET_IPS[it]} <<EOF
  iscsiadm --mode node --targetname ${FAILURE_TARGET_NAMES[it]} --portal $ISCSI_SERVER_IP:3260 --logout
  sleep 2
EOF
 let "it+=1"
done

