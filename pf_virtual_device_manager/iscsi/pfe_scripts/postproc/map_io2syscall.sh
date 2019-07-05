#!/usr/bin/env bash

#./THISFILE IO_LOG STRACE_LOG 


IO_HEAD_FILE=$PFE_LOG_DIR/pfe_io_head_split_log.od
IO_DATA_FILE=$PFE_LOG_DIR/pfe_io_data_log.work.od
IO_DATA_RAW=$PFE_LOG_DIR/pfe_io_data_log.work
#TRACE_FILE=$PFE_LOG_DIR/strace-worklog.txt

#width of od data line in bytes;
#the first data line of a IO will be printed out in the formatted map
DATALINE_WIDTH=32
sudo od -Ad -v --width=$DATALINE_WIDTH -t x $IO_DATA_RAW  > $IO_DATA_FILE

PY_IO=$PFE_SCRIPT_DIR/postproc/format_iolog.py
PY_STRACE=$PFE_SCRIPT_DIR/postproc/format_strace.py
PY_PINTRACE=$PFE_SCRIPT_DIR/postproc/format_pintrace.py
PY_MAP=$PFE_SCRIPT_DIR/postproc/map_io2syscall.py
PY_FILTER=$PFE_SCRIPT_DIR/postproc/filter_pintrace.py #rm libc libpthread calls


FORMATTED_IO=$PFE_LOG_DIR/formatted.io.txt
FORMATTED_STRACE=$PFE_LOG_DIR/formatted.syscall.txt
FORMATTED_PINTRACE=$PFE_LOG_DIR/formatted.pintrace.txt
FORMATTED_MAP=$PFE_LOG_DIR/formatted.map.txt
FILTERED_MAP=$PFE_LOG_DIR/formatted.map.filtered
SIMPLE_MAP=$PFE_LOG_DIR/formatted.map.sim


#for manual test only;
if (( $# == 3 )); then
    IO_HEAD_FILE=$1
    IO_DATA_FILE=$2
    TRACE_FILE=$3
fi



#io:
$PY_IO $IO_HEAD_FILE $IO_DATA_FILE $DATALINE_WIDTH > $FORMATTED_IO
echo "io head log is : $IO_HEAD_FILE"
echo "io data log is : $IO_DATA_FILE"
echo "io data line width is: $DATALINE_WIDTH bytes"

if [ $PROFILER == "pintool" ];then
    echo "PROFILER is: $PROFILER"
    #pin trace:
    COMBINED_TRACE_FILE=$PFE_LOG_DIR/pintool.log.wk.all
    $PFE_SCRIPT_DIR/postproc/combine_pintraces.py $PFE_LOG_DIR > $COMBINED_TRACE_FILE
    $PY_PINTRACE $COMBINED_TRACE_FILE > $FORMATTED_PINTRACE 
    $PY_MAP $FORMATTED_IO $FORMATTED_PINTRACE > $FORMATTED_MAP
    $PY_FILTER $FORMATTED_MAP > $FILTERED_MAP #rm libc libpthread calls
    $PFE_SCRIPT_DIR/postproc/format.syscalliomap.py $FILTERED_MAP > $SIMPLE_MAP  #rm first 2 fields: ts, relative ts
    
    echo "call trace is : $COMBINED_TRACE_FILE"
    echo "output mapping to: $FORMATTED_MAP"
    echo "output filtered mapping to: $FILTERED_MAP"
    echo "output simplified mapping to: $SIMPLE_MAP_MAP"

elif [ $PROFILER == "strace" ]; then 
    echo "PROFILER is: $PROFILER"
    #strace 
    TRACE_FILENAME=strace-worklog.txt.*
    COMBINED_TRACE_FILE=$PFE_LOG_DIR/strace.log.wk.all
    $PFE_SCRIPT_DIR/postproc/combine_strace_files.py $PFE_LOG_DIR $TRACE_FILENAME > $COMBINED_TRACE_FILE
    $PY_STRACE $COMBINED_TRACE_FILE > $FORMATTED_STRACE
    $PY_MAP $FORMATTED_IO $FORMATTED_STRACE > $FORMATTED_MAP
    $PFE_SCRIPT_DIR/postproc/format.syscalliomap.py $FORMATTED_MAP > $SIMPLE_MAP  #rm first 2 fields: ts, relative ts

    echo "call trace is : $COMBINED_TRACE_FILE"
    echo "output mapping to: $FORMATTED_MAP"
    echo "output simplified mapping to: $SIMPLE_MAP_MAP"

else
    echo "PROFILER is: none"
fi





