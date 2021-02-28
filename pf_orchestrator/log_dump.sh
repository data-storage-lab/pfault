#!/bin/bash

# script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
source ./config.sh

# CURRENT_DIR=`pwd`
# PARENT_DIR=`dirname $CURRENT_DIR`
# CONFIG_DIR=$PARENT_DIR/configuration/config.sh
# source $CONFIG_DIR

echo "$(($DUMP_TIME-INJECTION_TIME-FAILURE_TIME)) seconds left to dump"
sleep $(($DUMP_TIME-INJECTION_TIME-FAILURE_TIME))

echo "Start dumping logs"
pssh -i -h /home/osboxes/log_generator/pssh_hosts lctl debug_kernel $LOG_DUMP_DIR/$CURR_TIME

echo "cleaning stage"
killall -9 io500 &>/dev/null
rm -rf $CLIENT_LUSTRE_MNT_PNT/*


