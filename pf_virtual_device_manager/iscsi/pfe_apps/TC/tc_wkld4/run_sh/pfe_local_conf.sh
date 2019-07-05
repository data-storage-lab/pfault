#!/usr/bin/env bash

#local configurations
#change all "/home/mzheng/..." paths to your local environment

########### select one failure type 
export THIS_FAIL_TYPE=0 
#Valid Fail Type:
#define PFE_NORMAL 0                #implementted 
#define PFE_BIT_CORRUPTION 1        #implementted
#define PFE_SHORN_WRITES 2          #implementted
#define PFE_FLYING_WRITES 3         #implementted
#define PFE_UNSERIALIZABLE_WRITES 4 #implementted;need $UNSERIAL_PATTERN 
#define PFE_METADATA_CORRUPTION 5   #same as 7  
#define PFE_DEAD_DEVICE 6           #same as 0
#define PFE_RET_ERRNO5 7            #default metadata corruption
#define PFE_RET_HANG 8              #special metadata corruption

########### enable one type4 pattern 
export UNSERIAL_PATTERN=small
#export UNSERIAL_PATTERN=medium
#export UNSERIAL_PATTERN=large

########### enable one Filesystem 
export PFE_FS=ext3 
#export PFE_FS=xfs

########### enable one cutting method 
export CUT_OPTION=EXHAUSTIVE_CUT #cut all 
#export CUT_OPTION=SAMPLING_CUT; export SAMPLE_PERCENTAGE=1  #sample N out of 100


######### profiling for worker: strace or pintool or none
#export PROFILER=pintool
#export PROFILER=strace #default
export PROFILER=none 

######### profiling for checker: strace or pintool or none
#export PROFILER_CK=pintool
#export PROFILER_CK=strace
export PROFILER_CK=none #default 


########### enable one initiator setup script 
#export INITIATOR_SETUP_FILE=initiator-setup-rhel.sh   #rhel 6 
#export INITIATOR_SETUP_FILE=initiator-restart-deb.sh  #deb 6 
export INITIATOR_SETUP_FILE=initiator-setup-deb.sh    #deb 7


########### specify repos dir 
export PFE_HOME_DIR=/home/mzheng/0repos/code/scsi-tool #!!!CHANGE TO YOUR PATH TO THE REPOS 
export PFE_USR_DIR=${PFE_HOME_DIR}/usr
export PFE_SCRIPT_DIR=${PFE_HOME_DIR}/pfe_scripts

#export APPS_MAIN_DIR=$PFE_HOME_DIR/pfe_apps
#export APPS_MAIN_DIR= /home/mzheng/Temp/tc_wkld4/
#export PFE_LOG_DIR=${APP_DIR}/logs  
#export PFE_LOG_DIR=~/pfe_logs
#if [ ! -d $PFE_LOG_DIR ];then
#    echo "no $PFE_LOG_DIR, creating one ..."
#    sudo mkdir $PFE_LOG_DIR
#    sudo chmod 777 $PFE_LOG_DIR
#fi


#export MNT=/mnt/iscsi-fs #initiator side mount point
export MNT=~/pfe_mnt #initiator side mount point
if [ ! -d $MNT ];then
    echo "no $MNT, creating one ..."
    sudo mkdir $MNT
    sudo chmod 777 $MNT
fi


########### enable one DB Application 
#tc_wkld4
export APP_DIR=/home/mzheng/tc_wkld4/ #!!!CHANGE TO YOUR PATH TO THE WORKLOAD

export DB_ENVIRONMENT=$MNT/myEnvironment
export TEST_DB_NAME=TC
#export PY_CHECKER=$PFE_SCRIPT_DIR/postproc/check_wkld4.py

#this path is defined in gen_img.sh
export PRISTINE_INSTALL_IMG=~/pfe_images/img.128M.empty.$PFE_FS

. $PFE_SCRIPT_DIR/pfe_internal_config.sh 

