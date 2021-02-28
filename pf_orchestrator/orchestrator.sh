#!/bin/bash

CURRENT_DIR=`pwd`
parent_dir=$(dirname $CURRENT_DIR)
cp $parent_dir/configuration/configuration.sh $CURRENT_DIR/config.sh
source ./config.sh

# CURRENT_DIR=`pwd`
# PARENT_DIR=`dirname $CURRENT_DIR`
# CONFIG_DIR=$PARENT_DIR/configuration/config.sh
# source $CONFIG_DIR

# CURR_TIME=${CURR_TIME:=0}

pssh -i -h $(pwd)/pssh_hosts scp -r $ISCSI_SERVER_USER@$ISCSI_SERVER_IP:$parent_dir $PFAULT_DIR

CURR_TIME=0     
echo "Workload Finished $CURR_TIME/$RUN_TIME."
while [ "$CURR_TIME" -lt "$RUN_TIME" ]; do  
        
INJECTION_TIME=$((0 + $RANDOM % $DUMP_TIME))
# FAILURE_TIME=${FAILURE_TIME:=$((0 + $RANDOM % $(($DUMP_TIME-$INJECTION_TIME)) )) }

# run aging workload on client node and 
echo "ssh client"
ssh ${CLIENT_USER}@${CLIENT_IP} <<EOF
    source $PFAULT_DIR/pf_orchestrator/config.sh
    # nohup $PFAULT_DIR/pf_orchestrator/client_workload.sh >a.log 2>&1 </dev/null &
    nohup $PFAULT_DIR/pf_pfs_worker/pfs_worker_age.sh >a.log 2>&1 </dev/null &
    sleep 60
    echo "Start dumping logs: 1/3"
    pssh -i -h $PFAULT_DIR/pf_orchestrator/pssh_hosts lctl debug_kernel $LOG_DUMP_DIR/${CURR_TIME}_1
EOF

echo "$INJECTION_TIME seconds left to injection failure"
sleep $INJECTION_TIME 

# Select a node to inject fault
ssh ${MDS_USER}@${MDS_IP} <<EOF
    source $PFAULT_DIR/pf_orchestrator/config.sh
    nohup bash $PFAULT_DIR/pf_failure_state_emulator/${FAULT_MODEL}.sh
    sleep 3
EOF

# Run PFS checker
ssh ${MDS_USER}@${MDS_IP} <<EOF
    source $PFAULT_DIR/pf_orchestrator/config.sh
    $PFAULT_DIR/pf_pfs_checker/$PFS_CHECKER
    sleep 3
EOF

ssh ${CLIENT_USER}@${CLIENT_IP} <<EOF
    source $PFAULT_DIR/pf_orchestrator/config.sh
    echo "Start dumping logs 2/3"
    pssh -i -h $PFAULT_DIR/pf_orchestrator/pssh_hosts lctl debug_kernel $LOG_DUMP_DIR/$CURR_TIME
EOF

# Run check workload
ssh ${CLIENT_USER}@${CLIENT_IP} <<EOF
    source $PFAULT_DIR/pf_orchestrator/config.sh
    nohup $PFAULT_DIR/pf_pfs_worker/pfs_worker_verifiable.sh >a.log 2>&1 </dev/null &
    sleep 60
EOF

echo "$(($DUMP_TIME-INJECTION_TIME)) seconds left to dump"
sleep $(($DUMP_TIME-INJECTION_TIME))

ssh ${CLIENT_USER}@${CLIENT_IP} <<EOF

    echo "Start dumping logs"
    pssh -i -h $PFAULT_DIR/pf_orchestrator/pssh_hosts lctl debug_kernel $LOG_DUMP_DIR/$CURR_TIME

    echo "cleaning stage"
    # killall -9 io500 &>/dev/null
    rm -rf $CLIENT_LUSTRE_MNT_PNT/*
EOF

let "CURR_TIME+=1"
echo "A Workload Finished $CURR_TIME/$RUN_TIME."

done