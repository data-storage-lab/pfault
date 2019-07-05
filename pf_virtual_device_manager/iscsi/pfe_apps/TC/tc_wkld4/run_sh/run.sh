#!/bin/bash

absme=`readlink -f $0`
abshere=`dirname $absme`
. $abshere/pfe_local_conf.sh
. $abshere/w4_env_conf.sh


LOGS_DIR=~/pfe_logs
if [ ! -d $LOGS_DIR ];then
    echo "no $LOGS_DIR, creating one ..."
    sudo mkdir $LOGS_DIR
    sudo chmod 777 $LOGS_DIR
fi


#echo "Test N_KEY_PER_TXN from $start_size to $end_size, double every time"
#read -p "Press Enter to continue"


it=1
it_num=1 #total iteration number
while [ $it -le $it_num ]; do

  ########### add app-specific env var here
  #export N_KEY_PER_TXN=$count
  export TC_WKLD4_DB_FILE=$DB_ENVIRONMENT/casket.tcb
  ###########

    #ts of this run
    THISDATE=`date +"%y%m%d"`
    THISTIME=`date +"%T" | sed s/":"//g`
    THIS=$THISDATE$THISTIME
    #THIS=test

  ########### log dir for this config
  export PFE_LOG_DIR=$LOGS_DIR/logs-tc-wkld4_THR-${N_THR}-TXN-${N_TXN_PER_THR}-KEY-${N_KEY_PER_TXN}_fail-$THIS_FAIL_TYPE-unseri-$UNSERIAL_PATTERN-fs-$PFE_FS-cutopt-$CUT_OPTION-${SAMPLE_PERCENTAGE=100}.$THIS
  ###########

  #update PFE_LOG_DIR related config
  . $PFE_SCRIPT_DIR/pfe_internal_config.sh 

  echo $PFE_LOG_DIR
  rm -rf $PFE_LOG_DIR/*
  if [ ! -d $PFE_LOG_DIR ]; then
    mkdir $PFE_LOG_DIR
  fi

  cp $abshere/pfe_local_conf.sh $PFE_LOG_DIR
  cp $abshere/w4_env_conf.sh $PFE_LOG_DIR

  $PFE_SCRIPT_DIR/run-1.simple.sh
  $PFE_SCRIPT_DIR/run-2.simple.sh
  $PFE_SCRIPT_DIR/run-3.simple.sh
  #$PFE_SCRIPT_DIR/run-4.simple.sh

#  date
#  cd $PFE_SCRIPT_DIR/standalone_w4checker
#  ./checker_driver_singlelog.sh $PFE_LOG_DIR
#  date
  

#  count=$((2*count))
  it=$((it+1))
done

