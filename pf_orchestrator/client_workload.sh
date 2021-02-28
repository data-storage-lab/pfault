#!/bin/bash

# script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
source ./config.sh

# CURRENT_DIR=`pwd`
# PARENT_DIR=`dirname $CURRENT_DIR`
# CONFIG_DIR=$PARENT_DIR/configuration/config.sh
# source $CONFIG_DIR

# Load openmpi 
module load mpi/openmpi-x86_64

echo "cleaning data"
rm -rf $CLIENT_LUSTRE_MNT_PNT/*

# Will be substituted in formal version
echo "Copying IO500 to client mount point."
cp -r $USER$IO500 $CLIENT_LUSTRE_MNT_PNT


echo "Clear log buffer on each node."
pssh -i -h /home/osboxes/pssh_hosts lctl clear

echo "Start workload at ${CLIENT_LUSTRE_MNT_PNT}${IO500}."
cd $CLIENT_LUSTRE_MNT_PNT$IO500 && ./io500 $INI_FILE &

