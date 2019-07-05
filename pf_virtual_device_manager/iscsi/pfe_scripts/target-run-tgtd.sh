#!/usr/bin/env bash

. $PFE_SCRIPT_DIR/pfe_helper.sh

#echo "### start tgtd process in the foreground"
# "-f, --foreground        make the program run in the foreground\n"
# "-d, --debug debuglevel  print debugging information\n"

#lots of debug info
#sudo ../usr/tgtd -f -d 1   
#sudo ../usr/tgtd -f -d 1  2>&1 | tee log.tgtd 

#normal cmd
#sudo $PFE_USR_DIR/tgtd -f --pfe-io-header-log ${IO_HEAD_LOG} --pfe-io-data-log ${IO_DATA_LOG} --pfe-err-pattern ${ERR_PATTERN}  \
#    2>&1 | tee $PFE_LOG_DIR/log.tgtd 

#sudo $PFE_USR_DIR/tgtd  -f --pfe-io-header-log ${IO_HEAD_LOG} --pfe-fail-type-tgtd 5 \
#    --pfe-err-blk ${ERR_BLOCK_LOG} --pfe-io-data-log ${IO_DATA_LOG}\
sudo $PFE_USR_DIR/tgtd --pfe-io-header-log ${IO_HEAD_LOG} --pfe-fail-type-tgtd 0 \
    --pfe-err-blk ${ERR_BLOCK_LOG} --pfe-io-data-log ${IO_DATA_LOG} --pfe-enable-record 1\
    2>&1 | tee $PFE_LOG_DIR/log.tgtd 
#avoid too much log on real SSD
#sudo ../usr/tgtd -f    
