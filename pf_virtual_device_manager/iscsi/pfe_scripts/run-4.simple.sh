#!/usr/bin/env bash

. $PFE_SCRIPT_DIR/pfe_helper.sh

SCRIPT_NAME=$PFE_SCRIPT_DIR/4_repeat_replay.simple.sh
LOG_NAME=${PFE_LOG_DIR}/${STAGE_4_LOGNAME}.txt

$SCRIPT_NAME 2>&1 | tee $LOG_NAME
#$SCRIPT_NAME > $LOG_NAME 2>&1 



