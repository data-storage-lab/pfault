#!/usr/bin/env bash
#combine multip traces files and order the calls by timestamp

#./THISFILE LOG_DIR TRACE_FILENAME


PFE_SCRIPT_DIR=~/0repos/emulator-iscsi/pfe_scripts
PFE_LOG_DIR=$1
#TRACE_FILENAME=strace-worklog.txt.*
TRACE_FILENAME=$2

COMBINED_TRACE_FILE=$PFE_LOG_DIR/strace.log.wk.all


$PFE_SCRIPT_DIR/postproc/combine_strace_files.py $PFE_LOG_DIR $TRACE_FILENAME > $COMBINED_TRACE_FILE
