#!/usr/bin/env bash


APP_WORKER_EXE=$APP_DIR/worker.x


if [ $PROFILER == "pintool" ];then
    PINTOOL_LOG=$PFE_LOG_DIR/pintool.log.wk
    pin -injection child -t /home/zhengm/pin-2.13-62141-gcc.4.4.7-linux/source/tools/mai_PinTool/obj-intel64/mai_trace.so -logfile $PINTOOL_LOG -- $APP_WORKER_EXE

elif [ $PROFILER == "strace" ]; then

    #trace child processes; log to a single file
    #strace -tttTx -f -e write=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -o $PFE_LOG_DIR/strace-worklog.txt $APP_WORKER_EXE

    #separate diff processes' syscalls to diff files
    strace -tttTx -ff -s 64 -e write=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -o $PFE_LOG_DIR/strace-worklog.txt $APP_WORKER_EXE

else
    $APP_WORKER_EXE
fi
