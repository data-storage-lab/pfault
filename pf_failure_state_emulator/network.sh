#!/bin/sh

source $PFAULT_DIR/configuration_example.sh
#cp $PFAULT_DIR/pf_failure_state_emulator/failure_node_configuration_template.sh as $PFAULT_DIR/pf_failure_state_emulator/failure_node_configuration.sh and fill it out 
source $PFAULT_DIR/pf_failure_state_emulator/failure_node_configuration.sh
it=0
while [ $it -lt $FAILURE_TARGET_CNT]
do
ssh ${FAILURE_TARGET_USERS[it]}@${FAILURE_TARGET_IPS[it]} <<EOF
        ifconfig ${FAILURE_TARGET_LNET_CARDS[it]} down
EOF
let "it+=1"
done

